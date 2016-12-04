import cv2
import numpy as np
from vehicle_detection import VehicleDetector 
from camera_calibration import CameraCalibration
from video import Video

if __name__ == "__main__":
    
    cascade_src = 'cars.xml'
    video_src = 'dataset/test.mp4'

    # cap = cv2.VideoCapture(video_src)
    video = Video(video_src)
    video.setVehicleDetector(cascade_src)
    vehicleDetector = VehicleDetector(cascade_src)
    cc = CameraCalibration()
    cameraMatrix = cc.projectionTransform()
    

    while True:
    	video.playVideo()

    cv2.destroyAllWindows()