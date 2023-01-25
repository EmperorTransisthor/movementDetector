import requests

HOST = '192.168.1.85'
URL = "/photo-upload"


def send_photo(photo_path):
    try:
        files = [('photo', ('photo.jpg', open(photo_path), 'rb'), 'image/jpeg')]
        requests.request("POST", HOST + URL, files=files)
    except:
        print("Cannot send request")
