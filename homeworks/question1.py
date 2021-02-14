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
img12 = cv2.absdiff(img1,img2)
img12 =cv2.cvtColor(img12, cv2.COLOR_BGR2GRAY)
# convert pixels with difference >10 to white and everything else to black
img12b = cv2.threshold(img12, 10, 255, cv2.THRESH_BINARY)[1]

img34 = cv2.absdiff(img3,img4)
img34 =cv2.cvtColor(img34, cv2.COLOR_BGR2GRAY)
img34b = cv2.threshold(img34, 10, 255, cv2.THRESH_BINARY)[1]

# plot results
fig = plt.figure(figsize=(19.20,10.80))
plt.subplot(121),plt.imshow(img12b,cmap='gray'), plt.title('Painting1')
plt.subplot(122),plt.imshow(img34b,cmap='gray'), plt.title('Painting2')
plt.show()
