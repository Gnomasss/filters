import random
from filters import readImg, rotate_image
import cv2
import os
import numpy as np
import time
import ctypes
import math

def transformation(imgs, imgf, t):
    heightf, widthf = imgf.shape[:2]
    heights, widths = imgs.shape[:2]
    heightmn = min(heightf, heights)
    widthmn = min(widthf, widths)
    if heights > heightmn:
        ris = (heights - heightf) // 2
        rif = 0
    else:
        rif = (heightf - heights) // 2
        ris = 0
    if widths > widthf:
        rjs = (widths - widthf) // 2
        rjf = 0
    else:
        rjf = (widthf - widths) // 2
        rjs = 0

    new_img = np.array(imgs[ris: ris + heightmn, rjs: rjs + widthmn] * (1 - t * 0.1) + imgf[rif:heightmn + rif, rjf:widthmn + rjf] * (0.1 * t),
                       dtype=np.uint8)

    return new_img


def transformation_img(img_paths, img_pathf):
    imgs = readImg(img_paths)
    imgf = readImg(img_pathf)
    for i in range(11):
        img = transformation(imgs, imgf, i)
        cv2.imshow('img', img)
        cv2.waitKey(1)
        time.sleep(1/10)
    return imgf

def flip(img_paths, img_pathf):
    for i in range(0, 361, 10):
        if i <= 180:
            img = rotate_image(img_paths, i)
        else:
            img = rotate_image(img_pathf, i)
        cv2.imshow('img', img)
        cv2.waitKey(1)
        time.sleep(1 / 30)

def getTransform(img_paths, img_pathf):
    p = random.randint(0, 1)
    if p == 0:
        transformation_img(img_paths, img_pathf)
    else:
        flip(img_paths, img_pathf)
