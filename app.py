# backend

from flask import Flask, render_template, request, jsonify
import base64
from google.cloud import vision
import os
import json
import requests

print(os.getcwd())
# put your google cloud credentials in the secret.json file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./GoogleCloud.json"

with open("./api.json") as f:
    data = json.load(f)

API_KEY = data["API_KEY"]
SEARCH_ENGINE_ID = data["SEARCH_ENGINE_ID"]


def google_image_search(query):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query,
        "searchType": "image",
        "num": 3  # number of images to return
    }
    response = requests.get(url, params=params)
    results = response.json()

    images = []
    if "items" in results:
        for item in results["items"]:
            images.append({
                "title": item["title"],
                "link": item["link"],   # direct image link
            })
    return images


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


# !!!!!! debug only: create a logo object to save api fee !!!!!!
        # https://console.cloud.google.com/
        # Create a Vision API image object
        image = vision.Image(content=image_data)
        # call the Vision API to detect labels
        client = vision.ImageAnnotatorClient()
        response = client.logo_detection(image=image)
        logos = response.logo_annotations



        # class Logo:
        #     def __init__(self, description, score):
        #         self.description = description
        #         self.score = score
        # logos = [Logo("nike", 0.978978979),Logo("google", 0.456456487)]
        # logos = [] # test case for no logos found
# !!!!!! debug only: create a logo object to save api fee !!!!!!







# !!!!!! debug only: create a logo object to save api fee !!!!!!
        print("Logos:")
        for logo in logos:
            print(logo.description)
            print(logo.score)
        
        # save all the logos in a list
        returned_data = []
        if len(logos) == 0:
            returned_data.append({
                "description": "",
                "score": -1
            }) # add feature to read the words on the logo, and search for it(google or USPTO trademark search)
        else:
            for logo in logos:
                returned_data.append({
                    "description": logo.description,
                    "score": logo.score,
                    # return the logo picture by using the google search api(first only, for testing)
                    "image": google_image_search(logo.description+"brand logo")
                })
        # print the returned data
        print("Returned data:", returned_data)

        # returned_data = [{'description': 'nike', 'score': 0.978978979, 'image': [{'title': 'Nike brand logo outlet', 'link': 'https://logos-world.net/wp-content/uploads/2020/04/Nike-Logo.png'}, {'title': 'Nike Logo Vector Black Background, Editorial Stock Photo ...', 'link': 'https://thumbs.dreamstime.com/b/web-183282388.jpg'}, {'title': 'Nike Logo - Nike Brand Logo with Swoosh Design - CleanPNG', 'link': 'https://banner2.cleanpng.com/20180920/yah/kisspng-nike-logo-image-swoosh-brand-nike-made-a-micro-climate-chair-that-will-help-kee-1713938322541.webp'}]}, {'description': 'google', 'score': 0.456456487, 'image': [{'title': 'Evolving the Google Logo Identity - Google Design', 'link': 'https://storage.googleapis.com/gd-prod/images/a910d418-7123-4bc4-aa3b-ef7e25e74ae6.faa49ab5e1fff880.webp'}, {'title': 'Google brand logo symbol design Royalty Free Vector Image', 'link': 'https://cdn4.vectorstock.com/i/1000x1000/47/88/google-brand-logo-symbol-design-vector-46334788.jpg'}, {'title': 'Evolving the Google Logo Identity - Google Design', 'link': 'https://storage.googleapis.com/gd-prod/images/a910d418-7123-4bc4-aa3b-ef7e25e74ae6.81843175e48a9129.webp'}]}]
# !!!!!! debug only: create a logo object to save api fee !!!!!!




        # turn returned_data into a json object and return it
        return jsonify(returned_data)

# test the app
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
    # app.run(host="0.0.0.0", port=8080, debug=True) # run on LAN