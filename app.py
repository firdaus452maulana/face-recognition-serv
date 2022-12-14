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

from recogImage import recog

app = Flask(__name__)


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
        # print(type(imagedata))
        imgnew = cv2.cvtColor(np.array(imagedata), cv2.COLOR_BGR2RGB)

        output = recog(imgnew)

        respons = {'output': output}

        return jsonify(respons)


if __name__ == "__main__":
    app.run(debug=True)
