import os
from PIL import Image

def compressImage(filepath, quality_percentage = 1):
    picture = Image.open(filepath)

    picture.save("resources/Compressed.jpg",
                 "JPEG",
                 optimize = True,
                 quality = quality_percentage)
