import cv2
from camera_calibration import CameraCalibration
from video import Video
from config import *
from velocity_calculator import SpeedEstimator

if __name__ == "__main__":
    
    cascade_src = 'cars.xml'
    video_src = VIDEO_SRC

    # cap = cv2.VideoCapture(video_src)
    video = Video(video_src)
    video.setVehicleDetector(cascade_src)
    cc = CameraCalibration()
    cameraMatrix = cc.projectionTransform()
    video.setSpeedEstimator(cameraMatrix) 
    

    while True:
    	if video.playVideo() == -1:
    		break

        # calculate the vehicle velocity
        bumperSides = video.vehicleDetector.bumperSides

    #     ret, img = cap.read()
    #     if (type(img) == type(None)):
    #         break
        
    #     img_cars = vehicleDetector.detect_cars(img.copy())
        


    #     cv2.imshow('video', img_cars)        
    #     if cv2.waitKey(33) == 27:
    #         break

    cv2.destroyAllWindows()