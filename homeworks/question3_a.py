# -*- coding: utf-8 -*-
"""
Homeworks - Question 3 (a)
"""
import cv2
from matplotlib import pyplot as plt

# read images in grayscale
img1= cv2.imread('./imagesHW/hw3_building.JPG')
img2= cv2.imread('./imagesHW/hw3_train.JPG')

# apply median filter with kernel 3 and 5
median13 = cv2.medianBlur(img1,3)
median23 = cv2.medianBlur(img2,3)

median15 = cv2.medianBlur(img1,5)
median25 = cv2.medianBlur(img2,5)

 # plot results
fig = plt.figure(figsize=(19.20,10.80))
plt.subplot(231),plt.imshow(img1), plt.title('Original1')
plt.subplot(232),plt.imshow(median13), plt.title('Median3')
plt.subplot(233),plt.imshow(median15), plt.title('Median5')
plt.subplot(234),plt.imshow(img2), plt.title('Original2')
plt.subplot(235),plt.imshow(median23), plt.title('Median3')
plt.subplot(236),plt.imshow(median25), plt.title('Median5')
plt.show()

