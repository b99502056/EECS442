import numpy as np
from config import *

class SpeedEstimator(object):
    def __init__(self, cameraMatrix):
        self.cameraMatrix = cameraMatrix
        self.cameraMatrixInv = np.linalg.pinv(cameraMatrix)
        print 'cameraMatrixInv\n', self.cameraMatrixInv
        # self.carWidthWorld = 180 # Car width assumption in real world. Unit: cm
        self.previousDepth = 0
        self.currentDepth = 0
        self.previous_count = 0
        self.curr_cm_depth = 0

    def vehicleSpeed(self, bumperSides, count):
        bumperSides[0].append(1)
        bumperSides[1].append(1)
        bumperLeft = np.array(bumperSides[0])
        bumperRight = np.array(bumperSides[1])

        bumperLeftWorld = self.cameraMatrixInv.dot(bumperLeft)
        bumperRightWorld = self.cameraMatrixInv.dot(bumperRight)

        # Scale bumperRightWorld such that it has the same z coordinate as bumperLeftWorld
        bumperRightWorld = bumperRightWorld * (bumperLeftWorld[2] / bumperRightWorld[2])


        # Scale both points such that their x coordinates difference is the same as the
        # assumed value
        scale = CAR_WIDTH_WORLD / (abs(bumperLeftWorld[0] - bumperRightWorld[0]))

        # print 'bumperRightWorld', bumperRightWorld * scale
        # print 'bumperLeftWorld', bumperLeftWorld * scale
        self.curr_cm_depth = scale * bumperLeftWorld[2]
        print "CurrentDepth: " , self.curr_cm_depth

        # real depth of the car is scale * z coordinate
        self.currentDepth = self.cm2mile(scale * bumperLeftWorld[2])
        
        if self.previousDepth == 0: # First loop, ignore
            self.previousDepth = self.currentDepth
            self.previous_count = count
            return 0
        else:
            speed = (self.previousDepth - self.currentDepth) / self.s2hr((count - self.previous_count) / FRAME_PER_SEC)
            self.previousDepth = self.currentDepth
            self.previous_count = count
            print 'speed ', speed
            print '---------------------------'
            return speed

    def get_curr_cm_depth(self):
        return self.curr_cm_depth

    def cm2mile(self, cm):
        return cm*6.21371e-6

    def s2hr(self, s):
        return s/3600
