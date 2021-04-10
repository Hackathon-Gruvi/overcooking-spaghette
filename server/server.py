from flask import Flask
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)

@app.route('/')
def hello_world():
    file = open('../infohashes/torrents.json',mode='r')
    return file.read()