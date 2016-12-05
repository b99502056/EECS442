import cv2
from vehicle_detection import VehicleDetector 

class Video(object):
    def __init__(self, video_src):
        self.cap = cv2.VideoCapture(video_src)
        self.vehicleDetectorSet = False

    def playVideo(self):
        ret, img = self.cap.read()
        if (type(img) == type(None)):
            return -1

        if self.vehicleDetectorSet:
            img_cars = self.vehicleDetector.detectCars(img.copy())
            cv2.imshow('video', img_cars)
        else:
            cv2.imshow('video', img)

        if cv2.waitKey(33) == 27:
            return -1        

    def setVehicleDetector(self, cascade_src):
        if not self.vehicleDetectorSet:
            self.vehicleDetector = VehicleDetector(cascade_src)
            self.vehicleDetectorSet = True
