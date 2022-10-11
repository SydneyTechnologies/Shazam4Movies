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
    video = os.path.join(settings.BASE_DIR, "static/test3.MP4")
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
                if count % 500 == 0:
                    vision.imwrite(os.path.join(settings.BASE_DIR, f"static/actors/{count}.png"), currentFrame)
                    FRAMES.append(f"static/actors/{count}.png")
                if vision.waitKey(1) & 0xFF == ord("q"):
                    break
                if count > 1500:
                    break
            else:
                break
        

    identifyFaces()
    print(ACTORS_FOUND)
    captureInstance.release()
    
def identifyFaces():
    # upload images using pythons request library
    for frame in FRAMES:
        print(frame)
        files = {'imageUploadForm': open(os.path.join(settings.BASE_DIR, frame),'rb')}
        response= requests.post(CELEBRITY_URL, files=files)
        soup = BeautifulSoup(response.content, 'html.parser')

        result_div = soup.find_all("div", {"class":"text-center", "id":"result"})[0]
        print(result_div)
        if response.status_code == 200:
            result = soup.find("div", {"class": "realCandidate"})
            if result != None:
                similarity = result.find(attrs= {"class" :"progress-bar"})['similarity']
                actor = result.find("p").text
                if not ACTORS_FOUND.__contains__(actor):
                    print(f"{actor}: {similarity}")
                    ACTORS_FOUND[actor] = similarity
