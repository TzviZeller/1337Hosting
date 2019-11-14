function loadFile() {

      var base64Img = "";
      var file = document.querySelector('input[type=file]').files[0];
      var reader = new FileReader();

      reader.addEventListener("load", function () {
      	base64Img = reader.result;
      	console.log(`Img: ${base64Img}`);
        $.ajax({
          type: 'POST',
            // See @app.route("/genImage", methods=['POST']) in backend file to see how this works
          url: "/genImage",
          data: JSON.stringify({img:base64Img}),
          contentType: 'application/json;charset=UTF-8',
          success: function(data) {
              console.log(data);
              alert(data.toString());
           location.href = "/gallery/" + data.new_gallery_id;
         },
          error: function(error) {
                console.log(error);
            }
        });
      }, false);
     if (file) {
         // convert file to base64 for ajax json post to Flask
       reader.readAsDataURL(file);
   }
}
