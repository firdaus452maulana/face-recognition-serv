# from flask import Flask, request
# from flask_restful import Resource, Api
# from flask_cors import CORS
#
# # Inisialisasi
# app = Flask(__name__)
#
# # inisialisasi object flask_restful
# api = Api(app)
#
# # inisialisasi object flask_cors
# CORS(app)
#
# class Resource(Resource):
#
import base64
import io

import cv2
import numpy as np
from PIL import Image
from flask import Flask, request, jsonify
import face_recognition
import os
import subprocess

from recogImage import recog

app = Flask(__name__)

# Encoding List Image Known
path = 'imageAttedance'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


encodeListKnown = findEncodings(images)
print('Encoding Complete')


@app.route("/")
def home():
    return "Hello, World!"


@app.route("/recog", methods=["POST"])
def recognition():
    if request.method == 'POST':
        input_data = request.get_json(force=True)
        # print(input_data)
        imgdata = base64.b64decode(input_data['image_base64'])
        # print(type(imgdata))
        imagedata = Image.open(io.BytesIO(imgdata))
        # imagedata.save("imageAttedance/newImage.jpg")
        # print(type(imagedata))
        imgnew = cv2.cvtColor(np.array(imagedata), cv2.COLOR_BGR2RGB)

        output = recog(encodeListKnown, classNames, imgnew)

        respons = {'output': output}

        return jsonify(respons)

@app.route("/regis", methods=["POST"])
def register():
    if request.method == 'POST':
        input_data = request.get_json(force=True)
        name = input_data['name']
        imgdata = base64.b64decode(input_data['image_base64'])
        imagedata = Image.open(io.BytesIO(imgdata))
        imagedata.save("imageAttedance/{}.jpg".format(name))

        respons = {
            'status': 'Success',
            'message': 'User Berhasil Ditambahkan!',
        }

        return jsonify(respons)


if __name__ == "__main__":
    app.run(debug=True)
