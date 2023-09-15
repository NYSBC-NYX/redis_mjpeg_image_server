from flask import Flask, Response
import redis
import time
from PIL import Image
from io import BytesIO
import numpy as np

app = Flask(__name__)
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
img_width = 1224
img_height = 1024
img_size = (img_width,img_height)
mode = 'RGB'
def generate_mjpeg():
    while True:
        image = redis_client.get('bzoom:RAW')  

        #convert raw image file to jpg

        # with open('output.jpg', 'rb') as f:
        #     image = f.read()
        if image:
            byteData = convert_image(image)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + byteData + b'\r\n\r\n')
        time.sleep(0.02)  # Adjust this delay as needed


def convert_image(data):
    image = Image.frombuffer("RGB", (1224, 1024), data)
# Convert the PIL Image to JPEG binary
    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    jpeg_binary = buffer.getvalue()

    # Convert the image to jpg format and get the data as bytes
    return jpeg_binary



@app.route('/video_feed')
def video_feed():
    
    return Response(generate_mjpeg(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')






if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)