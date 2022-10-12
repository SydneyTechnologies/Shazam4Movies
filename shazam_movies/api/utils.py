# this file will contain all the major utility functions that allow this program to function

import os
from pickle import FRAME
import time
from bs4 import BeautifulSoup
import requests
import cv2 as vision
from django.conf import settings

CLASSIFIER = "face.xml"
DEFAULT_WATCH_TIME = 300
CELEBRITY_URL = "https://starbyface.com/Home/LooksLikeByPhoto"
faceClassifier = vision.CascadeClassifier(os.path.join(settings.BASE_DIR, f"static/cascades/{CLASSIFIER}"))
FRAMES = []
ACTORS_FOUND = {}
def ReadVideo():
    video = os.path.join(settings.BASE_DIR, "static/test2.MP4")
    # limit the watch time of the function 
    deadline = time.time() + DEFAULT_WATCH_TIME
    # we first create a capture instance which will read(watch) our video 
    # video location refers to the location of the video in question
    captureInstance = vision.VideoCapture(video)
    # captureInstance.set(vision.CAP_PROP_FPS, 60)
    count = 0
    if captureInstance.isOpened:
        while time.time() < deadline:
            count += 1
            open, currentFrame = captureInstance.read()
            if open:
                if count % 200 == 0:
                    vision.imwrite(os.path.join(settings.BASE_DIR, f"static/actors/{count}.png"), currentFrame)
                    FRAMES.append(f"static/actors/{count}.png")
                if vision.waitKey(1) & 0xFF == ord("q"):
                    break
                if count > 2000:
                    break
            else:
                break
        

    identifyFaces()
    print(ACTORS_FOUND)
    captureInstance.release()
    
def identifyFaces():
    # upload images using pythons request library
    for frame in FRAMES:
        files = {'imageUploadForm': open(os.path.join(settings.BASE_DIR, frame),'rb')}
        response= requests.post(CELEBRITY_URL, files=files)
        soup = BeautifulSoup(response.content, 'html.parser')

        if response.status_code == 200:
            male = soup.find(id="male-celebs-result")
            female = soup.find(id="female-celebs-result")
            mCandidate = male.find("div", attrs={"class":"progress-bar"})
            fCandidate = female.find("div", attrs={"class":"progress-bar"})
            mPercentage = mCandidate.text.replace("\r", "").replace("\n", "").replace("%", "")
            fPercentage = fCandidate.text.replace("\r", "").replace("\n", "").replace("%", "")
            if int(mPercentage) > int(fPercentage):
                ACTORS_FOUND[f"{male.div['name']}"] = int(mPercentage)
            else:
                ACTORS_FOUND[f"{female.div['name']}"] = int(fPercentage)
