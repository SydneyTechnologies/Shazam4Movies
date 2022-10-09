import cv2 as vision
# image = vision.imread("test.JPG", 0)
# vision.imshow('graytest', image)
# vision.imwrite("graytest.png", image)
# vision.waitKey(0)
# vision.destroyAllWindows()


videoCapture = vision.VideoCapture("testing.MP4")
face_cascade = vision.CascadeClassifier("cascades/face.xml")

while(True):
    ret, frame = videoCapture.read()
    gray_frame = vision.cvtColor(frame, vision.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors = 10)
    for (x, y, w, h) in faces:
        print(x, y, w, h)
        vision.rectangle(frame, (x-5, y-5), (x + w, y + h), (0, 255, 0), 3)
        face = vision.imwrite("actor.png", frame[y:y+h, x:x+w])

    vision.imshow("video", frame)
    if vision.waitKey(1) & 0xFF == ord("q"):
        break



videoCapture.release()
vision.destroyAllWindows()


