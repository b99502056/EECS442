# -*- coding: utf-8 -*-

import numpy as np 
import cv2
from math import pi
print(cv2.__version__)

def hough_line(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    lines = cv2.HoughLinesP(edges, 1, pi/2, 2, None, 20, 1);
    edges = cv2.merge((edges, edges, edges))
    
    for line in lines[0]:
        if(abs(line[0] - line[2]) < 20):
            print line
            pt1 = (line[0],line[1])
            pt2 = (line[2],line[3])
            cv2.line(edges, pt1, pt2, (0,0,255), 3)

    return edges

def find_cars(img):
    cascade_src = 'cars.xml'
    
    car_cascade = cv2.CascadeClassifier(cascade_src)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
    cars = car_cascade.detectMultiScale(gray, 1.1, 1)

    return cars

    # for (x,y,w,h) in cars:
    #     cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)      
    
    # cv2.imshow('video', img)

    # while True:
    #     ret, img = cap.read()
    #     if (type(img) == type(None)):
    #         break
        
    #     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
    #     cars = car_cascade.detectMultiScale(gray, 1.1, 1)

    #     for (x,y,w,h) in cars:
    #         cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)      
        
    #     cv2.imshow('video', img)
        
    #     if cv2.waitKey(33) == 27:
    #         break

    # cv2.destroyAllWindows()



def distance_to_camera(knownWidth, focalLength, perWidth):
    # compute and return the distance from the maker to the camera
    return (knownWidth * focalLength) / perWidth



# initialize the known distance from the camera to the object
KNOWN_DISTANCE = 2.0 # unit: m
 
# initialize the known object width, which in this case, is the width of a car
KNOWN_WIDTH = 1.8 # unit: m
 
# initialize the list of images that we'll be using
# IMAGE_PATHS = ["images/2ft.png", "images/3ft.png", "images/4ft.png"]
IMAGE_PATHS = ["50cut.png", "52cut.png"]
 
# load the first image that contains an object that is KNOWN TO BE 2 feet
# from our camera, then find the paper marker in the image, and initialize
# the focal length
image = cv2.imread(IMAGE_PATHS[0])
cars = find_cars(image)
focalLength = (cars[0][2] * KNOWN_DISTANCE) / KNOWN_WIDTH

""" VIDEO """
# crop_x_start = 150
# crop_x_end = 430

# video_src = 'dataset/test.mp4'
# #video_src = 'dataset/video2.avi'

# cap = cv2.VideoCapture(video_src)

# while True:
#     ret, image = cap.read()
#     if (type(image) == type(None)):
#         break
    
#     crop = image[:,crop_x_start:crop_x_end]

#     # cars = car_cascade.detectMultiScale(crop, 1.1, 1, 0, (60,60))

#     cars = find_cars(crop)
#     # sorted with width and get the one with largest width
#     cars = sorted(cars, key=lambda one_car: one_car[2], reverse=True)

#     try:
#         car_x, car_y, car_w, car_h = cars[0]
#         car_pic = crop[car_y : car_y + car_h, car_x : car_x + car_w]
#         # sub_img = contour(car_pic)
#         sub_img = hough_line(car_pic)
#         image[car_y : car_y + car_h, crop_x_start + car_x : crop_x_start + car_x + car_w] = sub_img
#     except:
#         continue


#     cv2.rectangle(image, (car_x + crop_x_start, car_y), (car_x + crop_x_start + car_w, car_y + car_h), (0,0,255), 2)

#     cv2.imshow('video', image)       
#     if cv2.waitKey(33) == 27:
#         break




""" IMAGE """
crop_x_start = 150
crop_x_end = 430

# loop over the images
for imagePath in IMAGE_PATHS:
    # load the image, find the marker in the image, then compute the
    # distance to the marker from the camera
    image = cv2.imread(imagePath)
    cars = find_cars(image)
    meters = distance_to_camera(KNOWN_WIDTH, focalLength, cars[0][2])
 
    # draw a bounding box around the image and display it
    # for (x,y,w,h) in cars:
    #     cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
    car_x, car_y, car_w, car_h = cars[1]
    car = cars[1]
    x = car[0]
    y = car[1]
    w = car[2]
    h = car[3]
    cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)

    car_pic = image[y : y + h, x : x + w]
    sub_img = hough_line(car_pic)
    image[y : y + h, crop_x_start+car_x : crop_x_start+car_x+car_w] = sub_img

    # box = np.int0(cv2.cv.BoxPoints(marker))
    # cv2.drawContours(image, [box], -1, (0, 255, 0), 2)

    # cv2.putText(image, "%.2fm" % meters,
    #     (image.shape[1] - 200, image.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
    #     2.0, (0, 255, 0), 3)
    cv2.putText(image, "%.2fm" % meters,
        (x, y+h), cv2.FONT_HERSHEY_SIMPLEX,
        0.8, (0, 255, 0), 2)

    cv2.imshow("image", sub_img)
    cv2.waitKey(0)