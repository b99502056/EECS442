# -*- coding: utf-8 -*-
import cv2
import numpy as np
from math import pi
from config import *

class Length(object):
    arr_len = 5
    pointer = 0
    is_first = True
    length_list = []

    def smooth(self, length):
        if self.is_first:
            self.length_list = length*np.ones(self.arr_len)
            self.pointer = 1
            self.is_first = False
            return length, True
        elif (length > MIN_LENGTH):
            self.length_list[self.pointer] = length
            self.pointer += 1
            if self.pointer == self.arr_len:
                self.pointer = 0
            return sum(self.length_list)/self.arr_len, True
        else:
            return self.length_list[self.pointer], False


class VehicleDetector(object):
    
    def __init__(self, cascade_src):
        self.len_object = Length()
        self.length = 0
        self.car_cascade = cv2.CascadeClassifier(cascade_src)
        self.car_speed = CAR_SPEED if 'CAR_SPEED' in globals() else []
        self.max_y = 0
        self.min_x = 0
        self.max_x = 0
        self.is_valid = False
        
    def detectCars(self, img, count):
        crop_x_start = CROP_X_START
        crop_x_end = CROP_X_END
        window_size = MIN_WINDOW_SIZE

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        crop = gray[:,crop_x_start:crop_x_end]

        cars = self.car_cascade.detectMultiScale(crop, 1.2, 2, 0, (window_size, window_size))
        # sorted with width and get the one with largest width
        cars = sorted(cars, key=lambda one_car: one_car[2], reverse=True)

        for (x,y,w,h) in cars:
            cv2.rectangle(img,(x+crop_x_start,y), (x+crop_x_start+w,y+h), (0,0,255), 2)

        if cars:
            car_x, car_y, car_w, car_h = cars[0]
            car_pic = crop[car_y:car_y+car_h, car_x:car_x+car_w]

            sub_img, length, min_x, max_x, max_y = self.contour(car_pic)

            self.length, self.is_valid = self.len_object.smooth(length)
            if self.is_valid:
                self.min_x = min_x
                self.max_x = max_x
                self.max_y = max_y
            print self.max_y

            img[car_y : car_y+car_h, crop_x_start+car_x : crop_x_start+car_x+car_w] = sub_img

        font = cv2.FONT_HERSHEY_SIMPLEX

        if self.car_speed:
            index = count*2/CAR_SPEED_PARAMETER
            speed = self.car_speed[index]
            print "actual speed: "+str(speed)
            cv2.putText(img, "actual speed: "+str(speed), (ACT_SPEED_X, ACT_SPEED_Y), font, 2, (0,0,0), 2, cv2.LINE_AA)
        
        cv2.putText(img, "pixel: "+str(self.length), (PIXEL_X, PIXEL_Y), font, 2, (0,0,0), 2, cv2.LINE_AA)
        return img, speed

    def bumperSidePoints(self):
        # contour[0]: left side of the bumper, contour[1]: right side of the bumper
        return [[self.min_x, self.max_y], [self.max_x, self.max_y]]

    def carWidthPixel(self):
        return self.length

    def find_ave_y(self, contour):
        return float(sum(pair[0][1] for pair in contour)) / len(contour)

    def find_max_length(self, contour):
        contour_x = sorted(contour, key=lambda pair: pair[0][0])

        mini = contour_x[0][0][0]
        maxi = contour_x[len(contour)-1][0][0]

        contour_y = sorted(contour, key=lambda pair: pair[0][1], reverse=True)
        maxy = contour_y[0][0][1]

        return maxi - mini, mini, maxi, maxy

    def find_length(self, contours, height):
        magic_number = MAGIC_NUMBER
        max_index = 0;
        max_y = self.find_ave_y(contours[0])

        for i in range(0, len(contours)):
            ave_y = self.find_ave_y(contours[i])
            # Find the countour cluster has maxmimum
            # Cannot be the dot around lower corners 
            if (ave_y > max_y and
                len(contours[i]) > 3 and
                ave_y < magic_number*height):
                max_index = i
                max_y = ave_y

        length, min_x, max_x, max_y = self.find_max_length(contours[max_index])
        return length, min_x, max_x, max_y

    def convert_binary(self, thresh):
        row = len(thresh)
        col = len(thresh[0])
        for i in range(0, row):
            for j in range(0, col):
                thresh[i][j] = 0 if thresh[i][j] == 255 else 255
        return thresh

    def contour(self, car_picture):
        kernel = np.ones((5,5), np.uint8)
        car_pic = cv2.GaussianBlur(car_picture, (17, 17), 1.2)
        erod =  cv2.erode(car_pic, kernel, iterations=1)

        ret, thresh = cv2.threshold(erod, 40, 255, cv2.THRESH_BINARY)
        # thresh = convert_binary(thresh)
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        erod = cv2.merge((erod, erod, erod))
        min_x = self.min_x
        max_x = self.max_x

        if contours:
            cv2.drawContours(erod, contours, -1, (0,255,0), 3)
            length, min_x, max_x, max_y = self.find_length(contours, len(car_picture[0]))
        else:
            length = 0
        return erod, length, min_x, max_x, max_y

    def hough_line(self, car_pic):
        edges = cv2.Canny(car_pic, 100, 200)
        lines = cv2.HoughLinesP(edges, 1, pi/180, 2, None, 30, 1);
        edges = cv2.merge((edges, edges, edges))
        for line in lines[0]:
            pt1 = (line[0],line[1])
            pt2 = (line[2],line[3])
            cv2.line(edges, pt1, pt2, (0,0,255), 3)
        return edges

    
