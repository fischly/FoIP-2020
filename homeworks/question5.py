# -*- coding: utf-8 -*-
"""
Homeworks - Question 5
"""
import cv2
from matplotlib import pyplot as plt
import numpy as np

# read image
img= cv2.imread('./imagesHW/hw5_insurance_form.JPG',0)
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(5,5)) # cross kernel
kernel1 = np.ones((3,3),np.uint8)
result=cv2.erode(img,kernel,iterations = 1)
#result=cv2.dilate(img,kernel1,iterations = 1)

image_center = tuple(np.array(img.shape[1::-1]) / 2)
rot_mat = cv2.getRotationMatrix2D(image_center, 2, 1.0)
result = cv2.warpAffine(result, rot_mat, img.shape[1::-1], borderValue=(255,255,255))

# plot results
fig = plt.figure(figsize=(19.20,10.80))
plt.subplot(121),plt.imshow(img, cmap='gray'), plt.title('Original')
plt.gca().axis("off")
plt.subplot(122),plt.imshow(result, cmap='gray'), plt.title('Edited')
plt.gca().axis("off")
plt.show()

# save resulted image
plt.imsave("restored.jpg", result, cmap = 'gray')