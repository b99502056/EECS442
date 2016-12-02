# -*- coding: utf-8 -*-

import cv2
import numpy as np
from math import pi

def hough_line(car_pic):
    edges = cv2.Canny(car_pic, 100, 200)
    lines = cv2.HoughLinesP(edges, 1, pi/180, 2, None, 30, 1);
    edges = cv2.merge((edges, edges, edges))
    for line in lines[0]:
        pt1 = (line[0],line[1])
        pt2 = (line[2],line[3])
        cv2.line(edges, pt1, pt2, (0,0,255), 3)
    return edges

def find_ave_y(contour):
    return float(sum(pair[0][1] for pair in contour)) / len(contour)

def find_max_length(contour):
    contour = sorted(contour, key=lambda pair: pair[0][0])

    mini = contour[0][0][0]
    maxi = contour[len(contour)-1][0][0]

    return maxi - mini

def find_length(contours, height):
    magic_number = 0.85
    max_index = 0;
    max_y = find_ave_y(contours[0])

    for i in range(0, len(contours)):
        ave_y = find_ave_y(contours[i])

        # Find the countour cluster has maxmimum
        # Cannot be the dot around lower corners 
        if (ave_y > max_y and
            len(contours[i]) > 6 and
            ave_y < magic_number*height):
            max_index = i
            max_y = ave_y

    length = find_max_length(contours[max_index])
    if length <= 30:
        print contours[max_index]

    return length

def convert_binary(thresh):
    row = len(thresh)
    col = len(thresh[0])
    for i in range(0, row):
        for j in range(0, col):
            thresh[i][j] = 0 if thresh[i][j] == 255 else 255
    return thresh

def contour(car_picture):
    kernel = np.ones((5,5), np.uint8)
    car_pic = cv2.GaussianBlur(car_picture, (17, 17), 1)
    erod =  cv2.erode(car_pic, kernel, iterations=1)

    ret, thresh = cv2.threshold(erod, 40, 255, cv2.THRESH_BINARY)
    # thresh = convert_binary(thresh)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    erod = cv2.merge((erod, erod, erod))
    cv2.drawContours(erod, contours, -1, (0,255,0), 3)
    length = find_length(contours, len(car_picture[0]))
    return erod, length

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
            return length
        elif (length > 30):
            self.length_list[self.pointer] = length
            self.pointer += 1
            if self.pointer == self.arr_len:
                self.pointer = 0
            return sum(self.length_list)/self.arr_len
        else:
            return self.length_list[self.pointer]


if __name__ == "__main__":
    crop_x_start = 130
    crop_x_end = 460

    cascade_src = 'cars.xml'
    video_src = 'test.mp4'

    cap = cv2.VideoCapture(video_src)
    car_cascade = cv2.CascadeClassifier(cascade_src)
    len_object = Length()
    length = 0

    while True:
        ret, img = cap.read()
        if (type(img) == type(None)):
            break
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        crop = gray[:,crop_x_start:crop_x_end]

        cars = car_cascade.detectMultiScale(crop, 1.2, 2, 0, (80,80))

        # sorted with width and get the one with largest width
        cars = sorted(cars, key=lambda one_car: one_car[2], reverse=True)

        for (x,y,w,h) in cars:
            cv2.rectangle(img,(x+crop_x_start,y),(x+crop_x_start+w,y+h),(0,0,255),2)

        if cars:
            car_x, car_y, car_w, car_h = cars[0]
            car_pic = crop[car_y:car_y+car_h, car_x:car_x+car_w]

            # sub_img = hough_line(car_pic)
            sub_img, length = contour(car_pic)
            length = len_object.smooth(length)

            img[car_y : car_y+car_h, crop_x_start+car_x : crop_x_start+car_x+car_w] = sub_img

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(length), (100,270), font, 2, (0,0,0), 2, cv2.LINE_AA)

        cv2.imshow('video', img)        
        if cv2.waitKey(33) == 27:
            break

    cv2.destroyAllWindows()


