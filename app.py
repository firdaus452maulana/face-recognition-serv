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
from flask import Flask, request, jsonify, flash, redirect
from werkzeug.utils import secure_filename
import face_recognition
import os

from recogImage import recog

UPLOAD_FOLDER = 'imageTemp'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

        # Open Image and Encode that for create model
        curImg = cv2.imread(f'imageAttedance/{name}.jpg')
        img = cv2.cvtColor(curImg, cv2.COLOR_BGR2RGB)
        facesCurFrame = face_recognition.face_locations(img)
        if not facesCurFrame:
            os.remove("imageAttedance/{}.jpg".format(name))
            respons = {
                'status': 'Failed',
                'message': 'Wajah Tidak Ditemukan',
            }
            return jsonify(respons)
        encode = face_recognition.face_encodings(img)[0]
        encodeListKnown.append(encode)
        classNames.append(name)

        respons = {
            'status': 'Success',
            'message': 'User Berhasil Ditambahkan!',
        }

        return jsonify(respons)

@app.route("/recog-photo", methods=["POST"])
async def recognitionPhoto():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            img = cv2.imread(f'imageTemp/{filename}')
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            output = recog(encodeListKnown, classNames, img)
            respons = {'output': output}

            os.remove("imageTemp/{}".format(filename))
            return jsonify(respons)

@app.route("/regis-photo", methods=["POST"])
async def registerPhoto():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            img = cv2.imread(f'imageTemp/{filename}')
            cur_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            facesCurFrame = face_recognition.face_locations(cur_img)
            if not facesCurFrame:
                os.remove("imageTemp/{}".format(filename))
                respons = {
                    'status': 'Failed',
                    'message': 'Wajah Tidak Ditemukan',
                }
                return jsonify(respons)

            # Saving Image to folder
            name = request.form['name']
            formatFile = os.path.splitext(filename)[1]
            cv2.imwrite("imageAttedance/{}".format(name+formatFile), img)

            os.remove("imageTemp/{}".format(filename))
            encode = face_recognition.face_encodings(img)[0]
            encodeListKnown.append(encode)
            classNames.append(name)

            respons = {
                'status': 'Success',
                'message': 'User Berhasil Ditambahkan!',
            }
            return jsonify(respons)



if __name__ == "__main__":
    app.run(debug=True)
