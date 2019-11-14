import os
import re
import secrets

import redis
from flask import Flask, render_template, request, jsonify, Response
from base64 import b64decode, b64encode

cache_host = 'redis' if os.getenv('ENV') == 'docker' else 'localhost'

cache = redis.StrictRedis(host=cache_host, port=6379)

app = Flask(__name__)


# Handles the POST data from 'static/uploadImage.js'
# This is then uses to create the new gallery .html file.
# This will be changed later to incorporate more jinja templates (they're cool)
@app.route("/genImage", methods=['POST'])
def genImage():
    # get json POST data...
    base64_str = request.json.get('img', None)
    if not base64_str:
        return Response("Must provide 'img' field containing valid base64 data.", status=400)

    try:
        without_prefix = base64_str.find(',') + 1
        base64_image = b64encode(b64decode(base64_str[without_prefix:]))
    except Exception as e:
        return Response(f"Invalid base64 data: {e}", status=400)

    new_gallery_id = secrets.token_hex(6)
    cache.set(new_gallery_id, base64_image)
    return jsonify(dict(new_gallery_id=new_gallery_id))




# this handles displaying the homepage when being accessed from / (the default url)
@app.route("/")
def hello():
    return render_template('index.html')


# this handles all request on pages using /gallery/#####   #### = some integer
# it correctly routes the user to the image page they want to view
# should 404 if doesn't exist, can implement better solution later.
@app.route("/gallery/<string:image_id>")
def get_gallery_image(image_id):
    if not image_id:
        return Response(400, "Bad Request. Must provide image_id")

    image_content = cache.get(image_id)

    renderable_str = f'data:image/png;base64,{image_content.decode("utf-8")}'

    if not image_content:
        return render_template('404.html', file1="A sly fox stole the image, sorry!")
    return render_template('gallery.jinja2', image_id=image_id, image_content=renderable_str)


if __name__ == "__main__":
    app.config.update(
        PROPAGATE_EXCEPTIONS=True
    )

    app.run(host='0.0.0.0', port=os.getenv('PORT', 5000), debug=True)
