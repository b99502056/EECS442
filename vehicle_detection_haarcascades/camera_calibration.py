import numpy as np 
import scipy.io as sio

class CameraCalibration(object):
	def __init__(self):
		corners_img1 = sio.loadmat("dataset/corners1_img.mat")
		corners_img2 = sio.loadmat("dataset/corners2_img.mat")
		corners_img1 = corners_img1["corners1_img"]
		corners_img2 = corners_img2["corners2_img"]

		corners_img = np.concatenate((corners_img1, corners_img2), axis = 0) 

		# Length of a cell in checkerboard. Unit: cm
		cellLen = 2.14
		# Corresponding world coordinates of the corners clicked on the images
		# Squares at (3,2)(5,4)(4,3)(5,2)(2,4)(1,1)
		corners_world1 = cellLen * np.array([[4,2,0], [5,3,0], [8,6,0], [9,7,0], [6,4,0], [7,5,0], \
		    [8,2,0], [9,3,0], [2,6,0], [3,7,0], [0,0,0], [1,1,0]])
		corners_world1[:,2] = 60 * np.ones(12);

		corners_world2 = cellLen * np.array([[4,2,0], [5,3,0], [8,6,0], [9,7,0], [6,4,0], [7,5,0], \
		    [8,2,0], [9,3,0], [2,6,0], [3,7,0], [0,0,0], [1,1,0]])
		corners_world2[:,2] = 70 * np.ones(12);

		corners_world = np.concatenate((corners_world1, corners_world2), axis = 0) 

		# Number of data points
		n = corners_world1.shape[0]

		self.Pw = np.concatenate((corners_world, np.ones((2 * n,1))), axis = 1)
		self.Pi = np.concatenate((corners_img, np.ones((2 * n,1))), axis = 1)


	# Pw: world points, Pi: image points
	def projectionTransform(self):
		n = self.Pw.shape[0];
		A = np.zeros((2*n, 12));

		T = self.imgDataNormalization(self.Pi)
		U = self.worldDataNormalization(self.Pw)

		# Noramlized points
		Pin = np.transpose(np.dot(T, np.transpose(self.Pi)))
		Pwn = np.transpose(np.dot(U, np.transpose(self.Pw)))

		for i in range(n):
			alpha = Pwn[i,:]
			A[2*i, :] = np.concatenate([alpha, [0, 0, 0, 0], -Pin[i,0] * alpha]);
			A[2*i+1, :] = np.concatenate([[0, 0, 0, 0], -alpha, Pin[i,1] * alpha]);
			
		_, s, Vt = np.linalg.svd(A, full_matrices = True);
		V = np.transpose(Vt)
		r = s.shape[0]
		# Assuming H is unique, meaning the basis of N(A) is V_r+1.
		h = V[:, r - 1] / V[11, r - 1];
		H  = h.reshape(3, 4)

		# Denormalization
		H = np.linalg.inv(T).dot(H.dot(U))
		print "Camera Matrix: \n", H
		self.errorCalculation(H)

		return H

	def imgDataNormalization(self, Pi):
		n = Pi.shape[0]
		x = Pi[:, 0]
		y = Pi[:, 1]
		normalDist = 2**0.5

		meanX = np.sum(x) / n
		meanY = np.sum(y) / n
		# Translate so that meanX = 0, meanY = 0
		Tt = np.array([[1,0,-meanX],[0,1,-meanY],[0,0,1]])
		Pit = np.transpose(np.dot(Tt, np.transpose(Pi)))
		xt = Pit[:, 0]
		yt = Pit[:, 1]

		# Calculate the mean distance to the origin after translation
		meanDist = np.sum(np.sqrt(xt**2 + yt**2)) / n
		scale = normalDist / meanDist

		T = np.array([[scale,0,scale*-meanX],[0,scale,scale*-meanY],[0,0,1]])
		return T

	def worldDataNormalization(self, Pw):
		n = Pw.shape[0]
		x = Pw[:, 0]
		y = Pw[:, 1]
		z = Pw[:, 2]
		normalDist = 3**0.5

		meanX = np.sum(x) / n
		meanY = np.sum(y) / n
		meanZ = np.sum(z) / n
		# Translate so that meanX = 0, meanY = 0
		Ut = np.array([[1,0,0,-meanX],[0,1,0,-meanY],[0,0,1,-meanZ],[0,0,0,1]])
		Pwt = np.transpose(np.dot(Ut, np.transpose(Pw)))
		xt = Pwt[:, 0]
		yt = Pwt[:, 1]
		zt = Pwt[:, 2]


		meanDist = np.sum(np.sqrt(xt**2 + yt**2 + zt**2)) / n
		scale = normalDist / meanDist

		U = np.array([[scale,0,0,scale*-meanX],[0,scale,0,scale*-meanY],[0,0,scale,scale*-meanZ],[0,0,0,1]])
		return U

	def errorCalculation(self,H):
		calculatedImgPoints = H.dot(np.transpose(self.Pw))
		errorMatrix = calculatedImgPoints[0:2,:] - np.transpose(self.Pi)[0:2,:]
		RMSError = np.mean(np.sum(errorMatrix**2, 0)**0.5)
		# print "img points: \n", np.transpose(self.Pi)
		# print "calculatedImgPoints: \n", calculatedImgPoints
		print "Calibration RMS error: ", RMSError

	
