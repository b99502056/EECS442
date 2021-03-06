###########
# GENERAL PARAMETER
###########

MAGIC_NUMBER = 0.85
FRAME_PER_SEC = 29.97 # FPS for mp4 files
CAR_WIDTH_WORLD = 180 # unit: cm

# OUTPUT_VIDEO = 'output.avi'


###########
# VIDEO SPECIFIC PARAMETER
###########

# # test.mp4
# VIDEO_SRC = 'dataset/test.mp4'
# CROP_X_START = 130
# CROP_X_END = 460
# MIN_WINDOW_SIZE = 20
# MIN_LENGTH = 30
# PIXEL_X = 30
# PIXEL_Y = 70

# # MVI_3344.MOV
# # shape(1080, 1920)
# VIDEO_SRC = 'dataset/MVI_3344.MOV'
# CROP_X_START = 200
# CROP_X_END = 1800
# MIN_WINDOW_SIZE = 70
# MIN_LENGTH = 16


# car_and_speed.mp4
# shape(1080, 1920)
VIDEO_SRC = 'dataset/car_and_speed.mp4'
CROP_X_START = 500
CROP_X_END = 1900
MIN_WINDOW_SIZE = 50
MIN_LENGTH = 15
PIXEL_X = 100
PIXEL_Y = 270
ACT_SPEED_X = 100
ACT_SPEED_Y = 600
EST_SPEED_X = 100
EST_SPEED_Y = 400
# Split by 0.5 sec, start from 0 sec
CAR_SPEED_PARAMETER = 24
CAR_SPEED = [0,  0,  0,  0, 0,
             0,  1,  3, 5,  11,
             14, 18, 21, 24,
             28, 30, 32, 35,
             36, 38, 38, 38, 36, 35, 33,
             31, 27, 24, 19, 12,
             4,  0, 0, 0, 0, 0, 0, 0]
