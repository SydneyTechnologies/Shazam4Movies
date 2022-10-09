# this file will contain all the major utility functions that allow this program to function

import os
import time
import requests
import cv2 as vision
from django.conf import settings

CLASSIFIER = "face.xml"
DEFAULT_WATCH_TIME = 20
CELEBRITY_URL = "https://starbyface.com/Home/LooksLikeByPhoto"
faceClassifier = vision.CascadeClassifier(os.path.join(settings.BASE_DIR, f"static/cascades/{CLASSIFIER}"))
ACTORS_FOUND = []
def ReadVideo():
    video = os.path.join(settings.BASE_DIR, "static/testing.MP4")
    print(video)
    # limit the watch time of the function 
    deadline = time.time() + DEFAULT_WATCH_TIME
    # we first create a capture instance which will read(watch) our video 
    # video location refers to the location of the video in question
    captureInstance = vision.VideoCapture(video)
    while time.time() < deadline:
        open, currentFrame = captureInstance.read()
        # this create a gray scale version of the current frame
        grayCapture = vision.cvtColor(currentFrame, vision.COLOR_BGR2GRAY)
        # allows for face detection
        faces = faceClassifier.detectMultiScale(grayCapture, scaleFactor=1.2, minNeighbors=5)
        for x, y, w, h in faces:
            vision.rectangle(currentFrame, (x-5, y-5), (x + w, y + h), (0, 255, 0), 3)
            vision.imwrite(os.path.join(settings.BASE_DIR, "static/actors.png"), currentFrame[y:y+h, x:x+w])
            identifyFace()
    captureInstance.release()
    vision.destroyAllWindows()

def identifyFace():
    files = {'imageUploadForm': open(os.path.join(settings.BASE_DIR, "static/actors.png"),'rb')}
    response= requests.post(CELEBRITY_URL, files=files)
    if response.status_code == 200:
        ACTORS_FOUND.append("found an actor")
