import cv2
from vehicle_detection import VehicleDetector 
from velocity_calculator import SpeedEstimator
from config import *


class Video(object):
    def __init__(self, video_src, cascade_src, cameraMatrix):
        self.cap = cv2.VideoCapture(video_src)
        if "OUTPUT_VIDEO" in globals():
            self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.out = cv2.VideoWriter(OUTPUT_VIDEO, self.fourcc, FRAME_PER_SEC, (960, 540))
        
        self.vehicleDetector = VehicleDetector(cascade_src)
        self.speedEstimator = SpeedEstimator(cameraMatrix)
        self.count = 0

    def playVideo(self):
        ret, img = self.cap.read()
        if (type(img) == type(None)):
            return -1

        self.count = self.count + 1
        if self.count > 200 and self.count < 330:
            img = self.renderCars(img.copy())

            img = self.renderSpeed(img.copy())

            img_resize = cv2.resize(img, (960, 540), interpolation=cv2.INTER_CUBIC)
            cv2.imshow('video', img_resize)

            if 'self.out' in locals():
                self.out.write(img_resize)

            if cv2.waitKey(33) == 27:
                return -1        

    def renderCars(self, img):
        img_cars = self.vehicleDetector.detectCars(img)
        return img_cars

    def renderSpeed(self, img):
        bumperSides = self.vehicleDetector.bumperSidePoints()
        speed = self.speedEstimator.vehicleSpeed(bumperSides, FRAME_PER_SEC)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, "estimated speed: "+str(speed), (EST_SPEED_X, EST_SPEED_Y), font, 2, (0,0,0), 2, cv2.LINE_AA)

        return img