#! /usr/bin/env python3

import cv2, os
import numpy as np
from model import FacialExpressionModel

facec = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
model = FacialExpressionModel("model.json", "model_weights.h5")
font = cv2.FONT_HERSHEY_SIMPLEX

class VideoCamera(object):
    def __init__(self):
        #Default for Webcam
        self.video = cv2.VideoCapture(0)

        # For Example Videos
        #self.video = cv2.VideoCapture(os.getcwd() + '/videos/facial_exp.mkv')

    def __del__(self):
        self.video.release()

    # returns camera frames along with bounding boxes and predictions
    def get_frame(self):
        _, fr = self.video.read()
        gray_fr = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
        faces = facec.detectMultiScale(gray_fr, 1.3, 5)

        for (x, y, w, h) in faces:
            fc = gray_fr[y:y+h, x:x+w]

            roi = cv2.resize(fc, (48, 48))
            pred = model.predict_emotion(roi[np.newaxis, :, :, np.newaxis])

            cv2.putText(fr, pred, (x, y), font, 1, (255, 255, 0), 2)
            cv2.rectangle(fr,(x,y),(x+w,y+h),(255,0,0),2)

        #_, jpeg = cv2.imencode('.jpg', fr)
        #return jpeg.tobytes()
        return cv2.imshow("Expression Detection", fr)


def main(camera):
    while True:
        camera.get_frame()
        key=cv2.waitKey(1)

        if key == ord('q'):
            break

if __name__ == "__main__":
    main(VideoCamera())
