# -*- coding: utf-8 -*-
"""
Homeworks - Question 6
"""
import cv2
from matplotlib import pyplot as plt
import numpy as np

# read image
img= cv2.imread('./imagesHW/coins.JPG',0)
img = cv2.medianBlur(img,5)
edges = cv2.Canny(img,30,150)
circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 1, 100, param1=50,param2=30,minRadius=2,maxRadius=100)

# ensure at least some circles were found
if circles is not None:
   circles = np.uint16(np.around(circles))
   for i in circles[0,:]:
       # draw the outer circle
       cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
       # draw the center of the circle
       cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)
       
# plot results
fig = plt.figure(figsize=(19.20,10.80))       
plt.imshow(img, cmap='gray'), plt.title('Coins Found')
plt.gca().axis("off")
print("I found %i coins" % len(circles[0,:]))