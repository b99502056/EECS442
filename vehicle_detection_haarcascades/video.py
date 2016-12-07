import cv2
from vehicle_detection import VehicleDetector 
from config import *

class Video(object):
    def __init__(self, video_src, cameraMatrix):
        self.cap = cv2.VideoCapture(video_src)
        self.vehicleDetectorSet = False
        self.speedEstimatorSet = False
        self.cameraMatrix = cameraMatrix

    def playVideo(self):
        ret, img = self.cap.read()
        if (type(img) == type(None)):
            return -1

        if self.vehicleDetectorSet:
            img_cars = self.vehicleDetector.detectCars(img.copy())

            if self.speedEstimatorSet:
                bumperSides = self.vehicleDetector.bumperSides()
                img_cars = self.speedEstimator(bumperSides, FRAME_PER_SEC)


            img_resize = cv2.resize(img_cars, (960, 540), interpolation=cv2.INTER_CUBIC)
            cv2.imshow('video', img_resize)
        else:
            img_resize = cv2.resize(img, (960, 540), interpolation=cv2.INTER_CUBIC)
            cv2.imshow('video', img_resize)

        if cv2.waitKey(33) == 27:
            return -1        


    def setVehicleDetector(self, cascade_src):
        if not self.vehicleDetectorSet:
            self.vehicleDetector = VehicleDetector(cascade_src)
            self.vehicleDetectorSet = True

    def setSpeedEstimator(self, cameraMatrix):
        if not self.speedEstimatorSet:
            self.speedEstimator = SpeedEstimator(cameraMatrix)
            self.speedEstimatorSet = True