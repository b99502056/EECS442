import numpy as np


class SpeedEstimator(object):
	def __init__(self, cameraMatrix):
		self.cameraMatrix = cameraMatrix
		self.carWidthWorld = 180 # Car width assumption in real world. Unit: cm
		self.previousDepth = 0
		self.currentDepth = 0

	# def vehicleSpeed(self, bumperSides, fps):
