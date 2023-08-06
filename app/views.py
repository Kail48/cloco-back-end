from app import app
from flask import request, jsonify
@app.route("/")
def hello():
    return "hello"