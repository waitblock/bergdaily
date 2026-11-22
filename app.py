from flask import Flask
import fetch

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, World!"
