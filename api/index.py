from flask import Flask
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()

@app.route("/api/python")
def hello_world():
    return "<p>Hello, World!</p>"