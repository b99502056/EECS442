import cv2
from vehicle_detection import VehicleDetector 
from config import *

class Video(object):
    def __init__(self, video_src):
        self.cap = cv2.VideoCapture(video_src)
        if "OUTPUT_VIDEO" in globals():
            self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.out = cv2.VideoWriter(OUTPUT_VIDEO, self.fourcc, FRAME_PER_SEC, (960, 540))
        self.vehicleDetectorSet = False

    def playVideo(self):
        ret, img = self.cap.read()
        if (type(img) == type(None)):
            return -1

        if self.vehicleDetectorSet:
            img = self.vehicleDetector.detectCars(img.copy())

        img_resize = cv2.resize(img, (960, 540), interpolation=cv2.INTER_CUBIC)
        cv2.imshow('video', img_resize)

        if self.out:
            self.out.write(img_resize)

        if cv2.waitKey(33) == 27:
            return -1        


    def setVehicleDetector(self, cascade_src):
        if not self.vehicleDetectorSet:
            self.vehicleDetector = VehicleDetector(cascade_src)
            self.vehicleDetectorSet = True

