import requests

HOST = '192.168.1.85'
URL = "/photo-upload"
PHOTO_PATH = ''




def send_photo():
    try:
        files = [('photo', ('photo.jpg', open(PHOTO_PATH, 'rb'), 'image/jpeg'))]
        requests.request("POST", HOST + URL, files=files)
    except:
        print("Cannot send request")
