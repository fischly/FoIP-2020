# -*- coding: utf-8 -*-
"""
Homeworks - Question 2
"""
import cv2
from matplotlib import pyplot as plt

# read images in grayscale
img1= cv2.imread('./imagesHW/hw1_dark_road_1.JPG',0)
img2= cv2.imread('./imagesHW/hw1_dark_road_2.JPG',0)
img3= cv2.imread('./imagesHW/hw1_dark_road_3.JPG',0)

# plot images & their histograms
plt.subplot(231),plt.imshow(img1,cmap = 'gray'), plt.title('Original1')
plt.subplot(232),plt.imshow(img2,cmap = 'gray'), plt.title('Original2')
plt.subplot(233),plt.imshow(img3,cmap = 'gray'), plt.title('Original3')
plt.subplot(234),plt.hist(img1, bins=20), plt.title('Histogram1')
plt.subplot(235),plt.hist(img2, bins=20), plt.title('Histogram2')
plt.subplot(236),plt.hist(img3, bins=20), plt.title('Histogram3')
plt.show()

# apply global histogram equalization
hst1 = cv2.equalizeHist(img1)
hst2 = cv2.equalizeHist(img2)
hst3 = cv2.equalizeHist(img3)

# plot equalized images & their histograms
plt.subplot(231),plt.imshow(hst1,cmap = 'gray'), plt.title('Equalized1')
plt.subplot(232),plt.imshow(hst2,cmap = 'gray'), plt.title('Equalized2')
plt.subplot(233),plt.imshow(hst3,cmap = 'gray'), plt.title('Equalized3')
plt.subplot(234),plt.hist(hst1, bins=20), plt.title('Histogram1')
plt.subplot(235),plt.hist(hst2, bins=20), plt.title('Histogram2')
plt.subplot(236),plt.hist(hst3, bins=20), plt.title('Histogram3')
plt.show()

# apply locally adaptive histogram equalization
clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(5,5))
cl1 = clahe.apply(img1)
cl2 = clahe.apply(img2)
cl3 = clahe.apply(img3)

# plot equalized images & their histograms
plt.subplot(231),plt.imshow(cl1,cmap = 'gray'), plt.title('Equalized1')
plt.subplot(232),plt.imshow(cl2,cmap = 'gray'), plt.title('Equalized2')
plt.subplot(233),plt.imshow(cl3,cmap = 'gray'), plt.title('Equalized3')
plt.subplot(234),plt.hist(cl1, bins=20), plt.title('Histogram1')
plt.subplot(235),plt.hist(cl2, bins=20), plt.title('Histogram2')
plt.subplot(236),plt.hist(cl3, bins=20), plt.title('Histogram3')
plt.show()