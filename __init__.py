from flask import Flask, render_template, request, url_for, redirect
import os
import subprocess

app = Flask(__name__)


# Handles the POST data from 'static/uploadImage.js'
# This is then uses to create the new gallery .html file.
# This will be changed later to incorporate more jinja templates (they're cool)
@app.route("/genImage", methods=['POST'])
def genImage():
    # get json POST data...
    imgCode = request.json['img']
    if imgCode is not None:
        with open('../../../var/local/var.txt', 'r') as f:
            # find the .txt file holding our incrementation mechanism
            incrementNum = f.read().splitlines()
            if incrementNum > 0:
                # path to new image upload's template
                writepath =  '../../../../var/www/imageHot/imageHot/templates/gallery/' + str(incrementNum[0]) + ".html"
            else:
                f.close()
        with open(writepath, "a+") as f:
            # This is probably the worst possible way to do this
            # Going to look into transforming this into a jinja template to only replace the imgCode value
            # Anyway, this will write to the .html file to create the newly uploaded image's page.
            htmlHeaders = "<!doctype html><html lang='en'><head><meta charset='utf-8'><title>1337Site</title><meta name='description' content='We host images lulz'></head><body>\n"
            styles = '<link rel="stylesheet" href="https://code.getmdl.io/1.1.3/material.blue-green.min.css" /><link rel="stylesheet" href="{{ url_for(\'static\', filename=\'style.css\')}}" /><link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">    <link href="https://fonts.googleapis.com/css?family=Exo+2" rel="stylesheet">"\n'
            # javaScript = '<script src="https://code.jquery.com/jquery-3.1.1.min.js"></script><script src="https://cdn.jsdelivr.net/clipboard.js/1.5.16/clipboard.min.js"></script><script src="{{ url_for(\'static\', filename=\'clippy.js\')}} "></script>\n'
            htmlFooter = "</body></html>"
            imageBox = "<div id=\"experienceBox\" class=\"mdl-cell mdl-cell--4-col mdl-shadow--2dp\">\n"
            linkBox = "<div id=\"linkBox\" class=\"mdl-cell mdl-cell--4-col mdl-shadow--2dp\">\n"
            link = "<input class='mdl-textfield__input' id='link' type='text' value='http://104.131.183.72/gallery/" + str(incrementNum[0]) + "'/>"
            # linkLabel = "<label class='mdl-textfield__label' for='link'>Link </label>\n"
            # link64Chars = "<textarea class='mdl-textfield__input' id='64bitImg' style='overflow:scroll;' type='text' rows='3' value=' " + str(imgCode) + "'/>"
            # charLabel = "<label class='mdl-textfield__label' for='64bitImg'>Base64 </label>\n"
            f.write(htmlHeaders)
            f.write(styles)
            f.write(imageBox)
            f.write("<img src=\"" + str(imgCode) + "\"/>\n")
            f.write("</div>\n")
            f.write(linkBox)
            f.write(link)
            # f.write(linkLabel)
            f.write("</div>\n")
            # f.write(linkBox)
            # f.write(link64Chars)
            # f.write(charLabel)
            # f.write("</div>\n")
            # f.write(javaScript)
            f.write(htmlFooter)

            # After writing is over, run the bash script to clean up and increment...
            if(subprocess.call("../../../var/local/GenClean.sh", shell=True)):
                return str(incrementNum[0])
            else:
                return "1337:bashError"
    else:
        return 'No image code'

# this handles displaying the homepage when being accessed from / (the default url)
@app.route("/")
def hello():
    return render_template('index.html')

# this handles all request on pages using /gallery/#####   #### = some integer
# it correctly routes the user to the image page they want to view
# should 404 if doesn't exist, can implement better solution later.
@app.route("/gallery/<int:imageId>")
def galleryRoute(imageId):
    list1 = list()
    imageURL = "/var/www/imageHot/imageHot/templates/gallery/" + str(imageId) + ".html"
    if os.path.isfile(imageURL):
        return render_template("/gallery/" + str(imageId) + ".html")
    else:
        return render_template('404.html', file1="A sly fox stole the image, sorry!")


def getRandomNum():
    return 4

if __name__ == "__main__":
    app.config.update(
        PROPAGATE_EXCEPTIONS=True
    )
    app.run(debug=True)
