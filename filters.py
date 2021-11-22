import random

import cv2
import os
import numpy as np
import time
import ctypes
import math

def readImg(img_path):
    img = cv2.imread(img_path)

    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    w, h = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
    height, width = img.shape[:2]
    if width > w or height > h:
        img = cv2.resize(img, (int(w * 0.7), int(h * 0.7)))
    return img

def tile(img_path):
    img = readImg(img_path)
    height_old, width_old = img.shape[:2]
    SIZE = 10
    img = cv2.resize(img, ((width_old // SIZE) * SIZE, (height_old // SIZE) * SIZE))
    n, m = height_old // SIZE, width_old // SIZE
    for i in range(n):
        for j in range(m):
            mean = list(map(int, np.mean(np.mean(img[i * SIZE : (i + 1) * SIZE, j * SIZE : (j + 1) * SIZE], axis=1), axis=0)))
            #print(mean)
            img[i * SIZE : (i + 1) * SIZE, j * SIZE : (j + 1) * SIZE] = [[mean for _ in range(10)] for _ in range(10)]
            #img[i * SIZE : (i + 1) * SIZE, j * SIZE : (j + 1) * SIZE] =
    return img

def rotate_image(img_path, angle):
    img = readImg(img_path)
    img_center = tuple(np.array(img.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(img_center, angle, 1)
    result = cv2.warpAffine(img, rot_mat, img.shape[1::-1])
    return result

def rotate(img_path):
    for i in range(0, 361, 10):
        img = rotate_image(img_path, i)
        cv2.imshow('img', img)
        cv2.waitKey(1)
        time.sleep(1 / 30)


def twisting(img_path):
    img = readImg(img_path)
    height, width = img.shape[:2]
    new_img = np.zeros((height, width, 3), dtype=np.uint8)
    img_center = tuple(np.array(img.shape[0:2]) / 2)
    #print(new_img[0, 0], img[0, 0], end='\n')
    #print(img_center, height)
    for i in range(height):
        for j in range(width):
            angle = (math.pi / 256) * ((img_center[0] - i) ** 2 + (img_center[1] - j) ** 2) ** 0.5
            #angle = math.pi / 6
            ti = int((i - img_center[0]) * math.cos(angle) - (j - img_center[1]) * math.sin(angle) + img_center[0])
            tj = int((i - img_center[0]) * math.sin(angle) + (j - img_center[1]) * math.cos(angle) + img_center[1])
            if ti < height and tj < width and ti >= 0 and tj >= 0:
                new_img[ti, tj] = img[i, j]

    return new_img


def wave(img_path):
    img = readImg(img_path)
    height, width = img.shape[:2]
    new_img = np.zeros((height, width, 3), dtype=np.uint8)
    #img_center = tuple(np.array(img.shape[0:2]) / 2)
    for i in range(height):
        for j in range(width):
            #angle = (math.pi / 256) * ((img_center[0] - i) ** 2 + (img_center[1] - j) ** 2) ** 0.5
            # angle = math.pi / 6
            tj = j
            ti = int(i + 20 * math.sin((2 * j * math.pi) / 64))
            if ti < height and tj < width and ti >= 0 and tj >= 0:
                new_img[ti, tj] = img[i, j]

    return new_img

def glass(img_path):
    img = readImg(img_path)
    height, width = img.shape[:2]
    new_img = np.zeros((height, width, 3), dtype=np.uint8)
    for i in range(height):
        for j in range(width):
            ri = random.randint(0, 10) - 5
            rj = random.randint(0, 10) - 5
            if i + ri < height and j + rj < width and i + ri >= 0 and j + rj >= 0:
                new_img[i + ri, j + rj] = img[i, j]
    return new_img

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

    #new_img = np.zeros((heightmn, widthmn, 3), dtype=np.uint8)
    '''for i in range(heightmn):
        for j in range(widthmn):
            new_img[i, j] = imgs[i + ris, j + rjs] * (1 - t * 0.1) + imgf[i + rif, j + rjf] * (t * 0.1)'''
    new_img = np.array(imgs[ris: ris + heightmn, rjs: rjs + widthmn] * (1 - t * 0.1) + imgf[rif:heightmn + rif, rjf:widthmn + rjf] * (0.1 * t),
                       dtype=np.uint8)
    #new_img.dtype = np.uint8
    #print(new_img)
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



def getFilter(img_path):
    i = random.randint(0, 4)
    if i == 0:
        img = tile(img_path)
        cv2.imshow('img', img)
        cv2.waitKey(1)
        time.sleep(3)
    elif i == 1:
        rotate(img_path)
    elif i == 2:
        img = twisting(img_path)
        cv2.imshow('img', img)
        cv2.waitKey(1)
        time.sleep(3)
    elif i == 3:
        img = wave(img_path)
        cv2.imshow('img', img)
        cv2.waitKey(1)
        time.sleep(3)
    else:
        img = glass(img_path)
        cv2.imshow('img', img)
        cv2.waitKey(1)
        time.sleep(3)







if __name__ == '__main__':
    dir = './img/'
    ls = os.listdir(dir)
    for i in range(len(ls) - 1):
        img = transformation_img(dir + ls[i], dir + ls[i + 1])
        cv2.imshow('img', img)
        cv2.waitKey(1)
        time.sleep(3)

