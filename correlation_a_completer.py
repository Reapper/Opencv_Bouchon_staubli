#!/usr/bin/python3

# B. Vandeportaele 31/12/2019

import cv2 as cv
import numpy as np

import sys
import time

#################################################################


def processImage(image):
    templ = cv.imread('template_bouchon_mm.png')
    mask = cv.imread('template_mask_bouchon_mm.png')
    print("templ:"+str(templ))
    print("mask:"+str(mask))

    # recherche du motif dans l'image rectifiée
    dst = image
    trouve = 1

    # dst = cv.matchTemplate(image, mask, cv.TM_CCOEFF)
    # affichage de cercles
    x = 100
    y = 80
    d1 = 32
    d2 = 22
    dst = cv.circle(
        dst, ((int)(x+templ.shape[0]/2), int(y+templ.shape[1]/2)), int(d1/2), (0, 255, 0))
    dst = cv.circle(
        dst, ((int)(x+templ.shape[0]/2), int(y+templ.shape[1]/2)), int(d2/2), (0, 255, 0))

    return (dst, trouve, x, y)

#################################################################


for i in range(1, 7):
    image = cv.imread(f'imgs/fetch%s.jpeg' % i)
    dst, trouve, x, y = processImage(image)
    # sauvgarde image avec surimpression
    cv.imwrite('imabouchon1_rect_trouve.jpg', dst)
    cv.imshow("image", dst)
    key = cv.waitKey(0)
cv.destroyAllWindows()
