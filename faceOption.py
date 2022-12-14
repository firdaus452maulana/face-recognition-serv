import cv2
import numpy as np
import face_recognition
import os
import requests
import base64
import json
import threading
import io
from PIL import Image


def login():
    trig_api = 0
    cap = cv2.VideoCapture(0)

    def callAPI(img):
        res, img = cv2.imencode('.jpg', img)
        data = base64.b64encode(img).decode('utf-8')
        rawJson = {
            "image_base64": data
        }
        response_recognition = requests.post(url='http://127.0.0.1:5000/recog', data=json.dumps(rawJson))
        print(response_recognition.json())

    def initialize():
        print("Initialize . . .")

    face_recog_api = threading.Thread(target=initialize, name="Initialize")
    face_recog_api.start()

    while True:
        success, img = cap.read()
        # img = captureScreen()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        # encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        # for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        #     matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        #     faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        #     # print(faceDis)
        #     matchIndex = np.argmin(faceDis)
        #
        if facesCurFrame:
            # name = classNames[matchIndex].upper()
            # print(name)
            y1, x2, y2, x1 = facesCurFrame[0]
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            # cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            # markAttendance(name)

            if not face_recog_api.is_alive():
                face_recog_api = threading.Thread(target=callAPI, name="Face Recog API", args=(img,))
                face_recog_api.start()
                # print("ini jalan")
                # print(face_recog_api.is_alive())
            else:
                # print("ini else")
                # print(face_recog_api.is_alive())
                # cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                # cv2.putText(img, "Loading", (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                pass


        #     else:
        #         name = "PENGUNJUNG"
        #         # print(name)
        #         y1, x2, y2, x1 = faceLoc
        #         y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        #         cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        #         cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
        #         cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('Webcam', img)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        elif key == ord('c'):
            if facesCurFrame:
                print("Encoding image to Base64")
                # print(type(img))
                res, img = cv2.imencode('.jpg', img)
                data = base64.b64encode(img).decode('utf-8')
                trigger = True
                break

    if trigger:
        #     imgdata = base64.b64decode(data)
        #     # print(type(imgdata))
        #     imagedata = Image.open(io.BytesIO(imgdata))
        #     # print(type(imagedata))
        #     imgnew = cv2.cvtColor(np.array(imagedata), cv2.COLOR_BGR2RGB)
        # print(type(imgnew))
        print(data)

        rawJson = {
            "image_base64": data
        }
        response_recognition = requests.post(url='http://127.0.0.1:5000/recog', data=json.dumps(rawJson))
        print(response_recognition.json())


def unused():
    #
    # imgMessi = face_recognition.load_image_file('images/Lionel Messi.jpg')
    # imgMessi = cv2.cvtColor(imgMessi, cv2.COLOR_BGR2RGB)
    # imgTest = face_recognition.load_image_file('images/Cristiano Ronaldo.jpg')
    # imgTest = cv2.cvtColor(imgTest, cv2.COLOR_BGR2RGB)
    #
    # faceLoc = face_recognition.face_locations(imgMessi)[0]
    # encodeElon = face_recognition.face_encodings(imgMessi)[0]
    # cv2.rectangle(imgMessi, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255, 0, 255), 2)
    #
    # faceLocTest = face_recognition.face_locations(imgTest)[0]
    # encodeTest = face_recognition.face_encodings(imgTest)[0]
    # cv2.rectangle(imgTest, (faceLocTest[3], faceLocTest[0]), (faceLocTest[1], faceLocTest[2]), (255, 0, 255), 2)
    #
    # results = face_recognition.compare_faces([encodeElon], encodeTest)
    # faceDis = face_recognition.face_distance([encodeElon], encodeTest)
    # print(results, faceDis)
    # cv2.putText(imgTest, f'{results} {round(faceDis[0], 2)}', (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    #
    # cv2.imshow('Lionel Messi', imgMessi)
    # cv2.imshow('Lionel Messi Test', imgTest)
    # cv2.waitKey(0)

    # path = 'imageAttedance'
    # images = []
    # classNames = []
    # myList = os.listdir(path)
    # print(myList)
    # for cl in myList:
    #     curImg = cv2.imread(f'{path}/{cl}')
    #     images.append(curImg)
    #     classNames.append(os.path.splitext(cl)[0])
    # print(classNames)
    #
    # def findEncodings(images):
    #     encodeList = []
    #     for img in images:
    #         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #         encode = face_recognition.face_encodings(img)[0]
    #         encodeList.append(encode)
    #     return encodeList
    #
    #
    # encodeListKnown = findEncodings(images)
    # print('Encoding Complete')
    #
    # cap = cv2.VideoCapture(0)
    #
    # while True:
    #     success, img = cap.read()
    #     # img = captureScreen()
    #     imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    #     imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    #
    #     facesCurFrame = face_recognition.face_locations(imgS)
    #     encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
    #
    #     for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
    #         matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
    #         faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
    #         # print(faceDis)
    #         matchIndex = np.argmin(faceDis)
    #
    #         if matches[matchIndex]:
    #             name = classNames[matchIndex].upper()
    #             # print(name)
    #             y1, x2, y2, x1 = faceLoc
    #             y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
    #             cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    #             cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
    #             cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
    #             # markAttendance(name)
    #         else:
    #             name = "PENGUNJUNG"
    #             # print(name)
    #             y1, x2, y2, x1 = faceLoc
    #             y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
    #             cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    #             cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
    #             cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
    #
    #         cv2.imshow('Webcam', img)
    #         cv2.waitKey(1)

    # path = 'imageAttedance'
    # images = []
    # classNames = []
    # myList = os.listdir(path)
    # trigger = False
    # data = ''
    # print(myList)
    # for cl in myList:
    #     curImg = cv2.imread(f'{path}/{cl}')
    #     images.append(curImg)
    #     classNames.append(os.path.splitext(cl)[0])
    # print(classNames)
    pass
