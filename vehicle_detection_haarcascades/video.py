import cv2
import numpy as np

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
        self.speed = 0
        self.act_speed = 0
        self.curr_cm_depth = 0
        # [frame, currentDepth(cm), estimate_speed, actual_speed]
        self.record_array = np.array([self.count, self.curr_cm_depth, self.speed, self.act_speed])

    def playVideo(self):
        ret, img = self.cap.read()
        if (type(img) == type(None)):
            return -1

        self.count = self.count + 1
        if self.count > 246 and self.count < 330:
            img = self.renderCars(img.copy(), self.count)
            img = self.renderSpeed(img.copy(), self.count)
            self.record_array = np.vstack((
                self.record_array,
                [self.count, self.curr_cm_depth, self.speed, self.act_speed]))
            img_resize = cv2.resize(img, (960, 540), interpolation=cv2.INTER_CUBIC)
            cv2.imshow('video', img_resize)

            if 'self.out' in locals():
                self.out.write(img_resize)

            if cv2.waitKey(33) == 27:
                return -1        

    def renderCars(self, img, count):
        img_cars, self.act_speed = self.vehicleDetector.detectCars(img, count)
        return img_cars

    def renderSpeed(self, img, count):
        if self.vehicleDetector.is_valid:
            bumperSides = self.vehicleDetector.bumperSidePoints()
            self.speed = self.speedEstimator.vehicleSpeed(bumperSides, count)
            self.curr_cm_depth = self.speedEstimator.get_curr_cm_depth()
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, "estimated speed: "+ str(self.speed), (EST_SPEED_X, EST_SPEED_Y), font, 2, (0,0,0), 2, cv2.LINE_AA)
        return img

    def save_csv(self, csv_src):
        with open(csv_src, 'wb') as file:
            np.savetxt(file, self.record_array, delimiter=",")