import cv2

from camera_calibration import CameraCalibration
from video import Video
from config import *


if __name__ == "__main__":
    
    cascade_src = 'cars.xml'
    video_src = VIDEO_SRC
    csv_src = 'data.csv'

    # cap = cv2.VideoCapture(video_src)
    cc = CameraCalibration()
    cameraMatrix = cc.projectionTransform()

    video = Video(video_src, cascade_src, cameraMatrix)

    while True:
    	if video.playVideo() == -1:
    		break
    
    video.save_csv(csv_src)
    video.cap.release()

    if hasattr(video, 'out'):
        video.out.release()

    cv2.destroyAllWindows()