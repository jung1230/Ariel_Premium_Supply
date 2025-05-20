# backend

from flask import Flask, render_template, request
import base64
from google.cloud import vision

app = Flask(__name__)


@app.route("/") # root path / (e.g. http://127.0.0.1:8080/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if request.method == 'POST':
        data = request.get_json()
        imagelink = data['image']

        # Decode the base64 image
        # get the second part of the data"data:image/png;base64,iVBORw0KGg..."
        image_data = base64.b64decode(imagelink.split(',')[1]) 

# https://console.cloud.google.com/
        # # debug
        # # Save the image to a file
        # with open("image.png", "wb") as f:
        #     f.write(image_data)
        return "Image saved successfully", 200



# test the app
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)