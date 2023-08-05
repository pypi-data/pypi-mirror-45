#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import numpy as np 
import cv2
import dlib


class CSEffects:
    def __init__(self):
        hat = os.path.join(os.path.dirname(__file__), "hat.png")
        self.__hat_img = cv2.imread(hat, -1) if os.path.isfile(hat) else None

        predictor_path = os.path.join(os.path.dirname(__file__), "shape_predictor_5_face_landmarks.dat")
        self.__predictor = dlib.shape_predictor(predictor_path)

        self.__detector = dlib.get_frontal_face_detector()

        self.__img_path = None
        self.__img = None
        self.__r = None
        self.__g = None
        self.__b = None
        self.__a = None

        self.__is_draw_facepoints = False
        self.__is_draw_rectangle = False
        self.__is_draw_eyescenter = False
        self.__is_draw_background = False
        self.__is_split_color_channels = False

        self.__bgs = []

    def input(self, img):
        folder = os.path.dirname(img)
        if not folder:
            img = os.path.join(os.path.realpath("."), img)

        self.__img_path = img
        if os.path.isfile(img):
            self.__img = cv2.imread(img)
        return self

    def draw_facepoints(self):
        self.__is_draw_facepoints = True
        return self

    def draw_eyescenter(self):
        self.__is_draw_eyescenter = True
        return self

    def draw_background(self):
        self.__is_draw_background = True
        return self

    def draw_rectangle(self):
        self.__is_draw_rectangle = True
        return self

    def split_color_channels(self):
        self.__is_split_color_channels = True
        return self

    def output(self, img=None):
        if self.__img is None:
            return

        folder, filename = os.path.split(self.__img_path if img is None else img)
        if not folder:
            folder = os.path.realpath(".")
        name, ext = os.path.splitext(filename)
        if img is None:
            img = os.path.join(folder, "%s_output%s" % (name, ext))
        if not os.path.isdir(folder):
            os.makedirs(folder)

        self.__r, self.__g, self.__b, self.__a = cv2.split(self.__hat_img)

        rgb_hat = cv2.merge((self.__r, self.__g, self.__b))

        dets = self.__detector(self.__img, 1)
        for d in dets:
            x, y, w, h = d.left(), d.top(), d.right() - d.left(), d.bottom() - d.top()
            if self.__is_draw_rectangle:
                cv2.rectangle(self.__img, (x,y), (x+w,y+h), (255,0,0), 2, 8, 0)

            shape = self.__predictor(self.__img, d)
            if self.__is_draw_facepoints:
                for point in shape.parts():
                    cv2.circle(self.__img, (point.x, point.y), 3, color=(0,255,0))

            point1 = shape.part(0)
            point2 = shape.part(2)
            eyes_center = ((point1.x + point2.x)//2, (point1.y + point2.y)//2)
            if self.__is_draw_eyescenter:
                cv2.circle(self.__img, eyes_center, 3, color=(0,255,0))  

            factor = 1.5
            resized_hat_h = int(round(rgb_hat.shape[0]*w / rgb_hat.shape[1]*factor))
            resized_hat_w = int(round(rgb_hat.shape[1]*w / rgb_hat.shape[1]*factor))

            if resized_hat_h > y:
                resized_hat_h = y-1

            resized_hat = cv2.resize(rgb_hat, (resized_hat_w, resized_hat_h))

            mask = cv2.resize(self.__a, (resized_hat_w, resized_hat_h))
            mask_inv =  cv2.bitwise_not(mask)

            dh = 0
            dw = 0
            bg_roi = self.__img[y+dh-resized_hat_h:y+dh, (eyes_center[0]-resized_hat_w//3):(eyes_center[0]+resized_hat_w//3*2)]

            bg_roi = bg_roi.astype(float)
            mask_inv = cv2.merge((mask_inv,mask_inv,mask_inv))
            alpha = mask_inv.astype(float)/255

            alpha = cv2.resize(alpha, (bg_roi.shape[1], bg_roi.shape[0]))
            bg = cv2.multiply(alpha, bg_roi)
            bg = bg.astype('uint8')
            self.__bgs.append(bg)

            hat = cv2.bitwise_and(resized_hat, resized_hat, mask=mask)
            hat = cv2.resize(hat, (bg_roi.shape[1], bg_roi.shape[0]))
            add_hat = cv2.add(bg, hat)

            self.__img[y+dh-resized_hat_h:y+dh, (eyes_center[0]-resized_hat_w//3):(eyes_center[0]+resized_hat_w//3*2)] = add_hat

        cv2.imwrite(img, self.__img)

        if self.__is_split_color_channels:
            cv2.imwrite(os.path.join(folder, "%s_red.jpg" % name), self.__r)
            cv2.imwrite(os.path.join(folder, "%s_green.jpg" % name), self.__g)
            cv2.imwrite(os.path.join(folder, "%s_blue.jpg" % name), self.__b)
            cv2.imwrite(os.path.join(folder, "%s_alpha.jpg" % name), self.__a)

        if self.__is_draw_background:
            index = 0
            for bg in self.__bgs:
                index += 1
                cv2.imwrite(os.path.join(folder, "%s_background_%s.jpg" % (name, index)), bg)

        


