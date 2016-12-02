import numpy as np
import cv2

def find_marker(image):
	# convert the image to grayscale, blur it, and detect edges
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (5, 5), 5)
	edged = cv2.Canny(gray, 35, 50)
	
	kernel = np.ones((7,7), np.uint8)
	edged = cv2.morphologyEx(edged, cv2.MORPH_CLOSE,kernel)
	edged = cv2.dilate(edged, kernel, iterations = 1)
	# cv2.imshow('edged', edged)
	# cv2.waitKey(0)

	# find the contours in the edged image and keep the largest one;
	_, cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	c = max(cnts, key = cv2.contourArea)

	# compute the bounding box of the of the object region and return it
	return cv2.minAreaRect(c)

def distance_to_camera(knownHeight, focalLength, perHeight):
	# compute and return the distance from the maker to the camera
	# perHeight: height of the object in pixels
	return (knownHeight * focalLength) / perHeight




# initialize the known distance from the camera to the object, which
# in this case is 15 cm
KNOWN_DISTANCE = 30.0

# initialize the known object height, which in this case, the book is 11cm tall, 15.8cm wide
KNOWN_HEIGHT = 11.0

# initialize the list of images that we'll be using
IMAGE_PATHS = ["30.jpg", "15.jpg"]

# load the first image that contains an object that is KNOWN TO BE 15cm
# from our camera, then find the marker in the image, and initialize
# the focal length
image = cv2.imread(IMAGE_PATHS[0])
marker = find_marker(image)
focalLength = (marker[1][1] * KNOWN_DISTANCE) / KNOWN_HEIGHT
print 'focal length: ', focalLength 

# loop over the images
for imagePath in IMAGE_PATHS:
	# load the image, find the marker in the image, then compute the
	# distance to the marker from the camera
	image = cv2.imread(imagePath)
	marker = find_marker(image)
	cms = distance_to_camera(KNOWN_HEIGHT, focalLength, marker[1][1])

	# draw a bounding box around the image and display it
	box = np.int0(cv2.boxPoints(marker))
	cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
	cv2.putText(image, "%.2fcm" % cms,
		(image.shape[1] - 200, image.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
		2.0, (0, 255, 0), 3)
	cv2.imshow("image", image)
	cv2.waitKey(0)