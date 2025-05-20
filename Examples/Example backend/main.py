# backend

from flask import Flask

app = Flask(__name__)


@app.route("/") # root path / (e.g. http://127.0.0.1:8080/")
def home():
    return "Congratulations, tesst!" # return means response tp the client

@app.route("/<int:celsius>") # path with a parameter (e.g. http://127.0.0.1:8080/87")
def fahrenheit_from(celsius):
    """Convert Celsius to Fahrenheit degrees."""
    try:
        fahrenheit = float(celsius) * 9 / 5 + 32
        fahrenheit = round(fahrenheit, 3)  # Round to three decimal places
        return str(fahrenheit)
    except ValueError:
        return "invalid input"




# test the app
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)