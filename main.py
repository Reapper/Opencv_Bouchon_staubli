#!/bin/python3

from enum import Enum
import cv2 as cv
from cv2 import IMREAD_UNCHANGED
from cv2 import IMREAD_GRAYSCALE
from cv2 import getStructuringElement
from cv2 import MORPH_RECT
import numpy as np
from matplotlib import pyplot as plt


class MorphType():
    ERODE = 0
    DILATE = 1
    OPEN = 2
    CLOSE = 3


def MorphOp(imageSource,
            typeMorph,
            kernel=[3, 3],
            iterationErode=1,
            iterationDilate=1):

    if(typeMorph == MorphType.ERODE):
        kernel = np.ones((kernel[0], kernel[1]), np.uint8)
        imageDest = cv.erode(imageSource, kernel, iterations=iterationErode)

    elif(typeMorph == MorphType.DILATE):
        kernel = np.ones((kernel[0], kernel[1]), np.uint8)
        imageDest = cv.dilate(imageSource, kernel, iterations=iterationDilate)

    elif(typeMorph == MorphType.OPEN):
        kernel = np.ones((kernel[0], kernel[1]), np.uint8)
        imageErode = cv.erode(imageSource, kernel, iterations=iterationErode)
        imageDest = cv.dilate(imageErode, kernel, iterations=iterationDilate)

    elif(typeMorph == MorphType.CLOSE):
        kernel = np.ones((kernel[0], kernel[1]), np.uint8)
        imageDilate = cv.dilate(imageSource, kernel,
                                iterations=iterationDilate)
        imageDest = cv.erode(imageErode, kernel, iterations=iterationErode)

    else:
        imageDest = imageSource.copy()

    return imageDest


def correlation():
    image = cv.imread("./imgs/fetch.jpeg", IMREAD_UNCHANGED)
    imageGray = cv.imread("./imgs/fetch.jpeg", IMREAD_GRAYSCALE)

    ret, imageBin = cv.threshold(imageGray,
                                 127,
                                 255,
                                 cv.THRESH_BINARY+cv.THRESH_OTSU)

    imageOpen = MorphOp(imageBin, MorphType.OPEN, (4, 4), 1, 1)

    cv.imshow("image", image)
    cv.imshow("imageGray", imageGray)

    cv.imshow("imageOpen", imageOpen)
    cv.imshow("imageBin", imageBin)

    cv.waitKey(0)


correlation()
