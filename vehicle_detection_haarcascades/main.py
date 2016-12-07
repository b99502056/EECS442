import cv2
from camera_calibration import CameraCalibration
from video import Video
from config import *
from velocity_calculator import SpeedEstimator

if __name__ == "__main__":
    
    cascade_src = 'cars.xml'
    video_src = VIDEO_SRC

    # cap = cv2.VideoCapture(video_src)
    cc = CameraCalibration()
    cameraMatrix = cc.projectionTransform()

    video = Video(video_src, cameraMatrix)
    video.setVehicleDetector(cascade_src)
    # video.setSpeedEstimator(cameraMatrix) 
    

    while True:
    	if video.playVideo() == -1:
    		break
        # calculate the vehicle velocity
        bumperSides = video.vehicleDetector.bumperSides

    video.cap.release()

    if video.out:
        video.out.release()

    cv2.destroyAllWindows()