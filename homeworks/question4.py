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
    
    # perform this test for each pixel
    for y in range(im.shape[1]):
        for x in range(im.shape[0]):
            im[x, y] = im_d[x, y] if im[x, y] >= im_h[x, y] else im_e[x, y]
        
# plot results
fig = plt.figure(figsize=(19.20,10.80))
plt.subplot(121),plt.imshow(img,cmap='gray'), plt.title('Original')
plt.subplot(122),plt.imshow(im,cmap='gray'), plt.title('Edited')
plt.show()

# save resulting image
plt.imsave('./results/question_4_road_sign_school_blurry_filtered.jpg', im, cmap = 'gray')