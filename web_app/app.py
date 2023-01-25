from flask import Flask, render_template, request, jsonify, send_file, abort
import os
from time import time

from lora.gps import get_coords


PHOTO_PATH = '/resources/photo.jpg'

app = Flask(__name__)

""" Routes """

@app.route("/", methods=['GET'])
def index():
    photo = photo_exists()
    latitude, longitude, cord_valid = get_coordinates()
    return render_template('index.html',cord_valid=cord_valid,latitude=latitude,longitude=longitude,photo=photo)

@app.route("/photo", methods=['GET'])
def photo():
    if not photo_exists():
        abort(404, 'There is no photo in app')
    return send_file(
        get_photo_path(),
        mimetype='image/jpg',
        attachment_filename='photo.jpg'
    )

@app.route("/photo-upload", methods=['POST'])
def photo_upload():
    f = request.files['photo']
    f.save(get_photo_path())
    return jsonify("ok")


""" Other methods """

def photo_exists() -> bool:
    path = get_photo_path()
    if not os.path.exists(path):
        return False
    if os.stat(path)[8]+180 < time():
        return False
    return True

def get_photo_path():
    return os.getcwd() + PHOTO_PATH

def get_coordinates():
    lat, long = get_coords()
    cord_valid = True
    if lat == 0 and long == 0:
        lat = 52.22165186731319
        long = 21.00645902632439
        cord_valid = False
    return lat, long, cord_valid