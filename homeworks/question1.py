# -*- coding: utf-8 -*-
"""
Homeworks - Question 1
"""
import cv2
from matplotlib import pyplot as plt

# read images
img1= cv2.imread('./imagesHW/hw1_painting_1_reference.JPG')
img2= cv2.imread('./imagesHW/hw1_painting_1_tampered.JPG')
img3= cv2.imread('./imagesHW/hw1_painting_2_reference.JPG')
img4= cv2.imread('./imagesHW/hw1_painting_2_tampered.JPG')

# subtract images & convert to grayscale
img12 = cv2.subtract(img1,img2)
img12 =cv2.cvtColor(img12, cv2.COLOR_BGR2GRAY)
# convert 0 pixels to black and everything else to white
img12b = cv2.threshold(img12, 0, 255, cv2.THRESH_BINARY)[1]

img34 = cv2.subtract(img3,img4)
img34 =cv2.cvtColor(img34, cv2.COLOR_BGR2GRAY)
img34b = cv2.threshold(img34, 0, 255, cv2.THRESH_BINARY)[1]

# plot results
plt.subplot(121),plt.imshow(img12b,cmap='gray'), plt.title('Painting1')
plt.subplot(122),plt.imshow(img34b,cmap='gray'), plt.title('Painting2')
plt.show()