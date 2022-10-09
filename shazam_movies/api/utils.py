# this file will contain all the major utility functions that allow this program to function

import os
import time
from bs4 import BeautifulSoup
import requests
import cv2 as vision
from django.conf import settings

CLASSIFIER = "face.xml"
DEFAULT_WATCH_TIME = 90
CELEBRITY_URL = "https://starbyface.com/Home/LooksLikeByPhoto"
faceClassifier = vision.CascadeClassifier(os.path.join(settings.BASE_DIR, f"static/cascades/{CLASSIFIER}"))
ACTORS_FOUND = {}
def ReadVideo():
    video = os.path.join(settings.BASE_DIR, "static/test3.MP4")
    print(video)
    # limit the watch time of the function 
    deadline = time.time() + DEFAULT_WATCH_TIME
    # we first create a capture instance which will read(watch) our video 
    # video location refers to the location of the video in question
    captureInstance = vision.VideoCapture(video)
    while time.time() < deadline:
        open, currentFrame = captureInstance.read()
        # this create a gray scale version of the current frame
        dim = (int(currentFrame.shape[1] * 2), int(currentFrame.shape[0] * 2))
        resized = vision.resize(currentFrame, dim, interpolation = vision.INTER_AREA)
        grayCapture = vision.cvtColor(resized, vision.COLOR_BGR2GRAY)
        # allows for face detection
        faces = faceClassifier.detectMultiScale(grayCapture, scaleFactor=1.4, minNeighbors=5)
        for x, y, w, h in faces:
            # vision.rectangle(currentFrame, (x-5, y-5), (x + w, y + h), (0, 255, 0), 3)
            vision.imwrite(os.path.join(settings.BASE_DIR, "static/actors.png"), resized[y:y+h, x:x+w])
            identifyFace()
        

    print(ACTORS_FOUND)
    captureInstance.release()
    vision.destroyAllWindows()

def identifyFace():
    # upload images using pythons request library
    files = {'imageUploadForm': open(os.path.join(settings.BASE_DIR, "static/actors.png"),'rb')}
    response= requests.post(CELEBRITY_URL, files=files)
    soup = BeautifulSoup(response.content, 'html.parser')

    if response.status_code == 200:
        result = soup.find("div", attrs= {"class" :"candidate"})
        if result != None:
            similarity = result.find(attrs= {"class" :"progress-bar"})['similarity']
            actor = result.find("p").text
            if int(similarity) < 40:
                return 
            if not ACTORS_FOUND.__contains__(actor):
                print(f"{actor}: {similarity}")
                ACTORS_FOUND[actor] = similarity
