# -*- coding: utf-8 -*-
"""
Homeworks - Question 4
"""
import cv2
from matplotlib import pyplot as plt

# read image
img= cv2.imread('./imagesHW/hw3_road_sign_school_blurry.JPG',0)
im = img.copy()
W = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3)) # cross kernel

# apply the algorithm
for i in range(10):
    im_d = cv2.dilate(im,W,iterations = 1)
    im_e = cv2.erode(im,W,iterations = 1)
    im_h = cv2.addWeighted(im_d,0.5,im_e,0.5,0)
    if (im > im_h).all():
        im = im_d
    else:
        im = im_e
        
# plot results
fig = plt.figure(figsize=(19.20,10.80))
plt.subplot(121),plt.imshow(img,cmap='gray'), plt.title('Original')
plt.subplot(122),plt.imshow(im,cmap='gray'), plt.title('Edited')
plt.show()