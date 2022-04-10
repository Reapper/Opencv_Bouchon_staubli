#!/usr/bin/python3

# B. Vandeportaele 31/12/2019

from enum import Enum
import cv2 as cv
import numpy as np

import sys
import time


#################################################

class MorphType():
    ERODE = 0
    DILATE = 1
    OPEN = 2
    CLOSE = 3

#################################################


def colorName2Bin(colorName):
    if (colorName == "Red"):
        return f'{0xFF0000:0>24b}'
    elif(colorName == "Green"):
        return f'{0x00FF00:0>24b}'
    elif(colorName == "Blue"):
        return f'{0x0000FF:0>24b}'
    elif(colorName == "Orange"):
        return f'{0xFF7F00:0>24b}'

#################################################


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

#################################################


def create_pattern_and_mask(width, height, d1, d2, bgr_color_center=(0, 0, 0), bgr_color_contour=(0, 0, 0)):
    """Create new image(numpy array) filled with certain color in RGB"""
    # Create black blank image
    image = np.zeros((height, width, 3), np.uint8)
    cv.circle(image,
              (int(height/2),  int(width/2)),
              int(d1/2),
              (int(bgr_color_contour[0]),
               int(bgr_color_contour[1]),
               int(bgr_color_contour[2])),
              -1)

    cv.circle(image,
              (int(height/2),  int(width/2)),
              int(d2/2),
              (int(bgr_color_center[0]),
               int(bgr_color_center[1]),
               int(bgr_color_center[2])),
              -1)

    mask = np.zeros((height, width, 3), np.uint8)
    cv.circle(mask,
              (int(height/2),  int(width/2)),
              int(d1/2),
              (255, 255, 255),
              -1)

    return image, mask

#################################################


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

#################################################


listeColors = ["Blue", "Orange"]
# couleurs codées en sortie dans séquence de 0 à 8
# with open("listecolors.out", "wb") as file:
#     for i in listeColors:
#         file.write(i + ',')

listeRGB = []
positonBouchon = []
print('chargement depuis fichier listecolors.out')
filedata = np.genfromtxt('listecolors.out', delimiter=',').astype('uint8')
# il faut transformer en liste de array([114, 187,  71], dtype=uint8)
for i in range(0, 2):
    # listeRGB[i]=filedata[i]
    listeRGB.append(filedata[i])
print(listeRGB)

# synthese du motif et du masque
width, height = 32, 32
d1 = 32
d2 = 22
# utiliser listeRGB pour générer le masque!


templ, mask = create_pattern_and_mask(
    width, height, d1, d2, listeRGB[1], listeRGB[0])

cv.imwrite('template_bouchon_mm.png', templ)
cv.imwrite('template_mask_bouchon_mm.png', mask)

for i in range(1, 7):
    positonBouchon = []

    img_rgb = cv.imread(f'imgs/fetch%s.jpeg' % i)

    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)

    template = cv.imread('template_mask_bouchon_mm.png', 0)

    w, h = template.shape[::-1]

    cv.imshow("img_gray", img_gray)
    cv.imshow("template", template)

    res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
    threshold = 0.70
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

        positonBouchon.append([(pt[0] + int(w/2)), (pt[1] + int(h/2))])

        # cv.circle(img_rgb, (pt[0] + int(w/2), pt[1] +
        #           int(h/2)), int(h/2), (0, 0, 255), 2)

    print(f'fetch%s =' % i, positonBouchon)

    cv.imwrite(f'res%s.png' % i, img_rgb)
    cv.imshow("res", img_rgb)
    cv.waitKey(0)
    print(i)


for i in range(1, 7):
    image = cv.imread(f'imgs/fetch%s.jpeg' % i)
    dst, trouve, x, y = processImage(image)
    # sauvgarde image avec surimpression
    cv.imwrite('imabouchon1_rect_trouve.jpg', dst)
    cv.imshow("image", dst)
    key = cv.waitKey(0)
cv.destroyAllWindows()
