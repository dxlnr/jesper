from flask import Flask

from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def check():
    return "Jesper Backend Server up and running."


app.run(host="0.0.0.0", port=5000, debug=True)
