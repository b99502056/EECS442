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
		corners_world1[:,2] = 0 * np.ones(12);

		corners_world2 = cellLen * np.array([[4,2,0], [5,3,0], [8,6,0], [9,7,0], [6,4,0], [7,5,0], \
		    [8,2,0], [9,3,0], [2,6,0], [3,7,0], [0,0,0], [1,1,0]])
		corners_world2[:,2] = 10 * np.ones(12);

		corners_world = np.concatenate((corners_world1, corners_world2), axis = 0) 

		self.Pw = corners_world
		self.Pi = corners_img


	# Pw: world points, Pi: image points
	def projectionTransform(self):
		n = self.Pw.shape[0];
		A = np.zeros((2*n, 12));

		for i in range(n):
			alpha = np.append(self.Pw[i,:], 1)
			A[2*i, :] = np.concatenate([alpha, [0, 0, 0, 0], -self.Pi[i,0] * alpha]);
			A[2*i+1, :] = np.concatenate([[0, 0, 0, 0], -alpha, self.Pi[i,1] * alpha]);
			
		_, s, Vt = np.linalg.svd(A, full_matrices = True);
		V = np.transpose(Vt)
		r = s.shape[0]
		# Assuming H is unique, meaning the basis of N(A) is V_r+1.
		h = V[:, r - 1] / V[11, r - 1];
		H  = h.reshape(3, 4)

		return H

		




