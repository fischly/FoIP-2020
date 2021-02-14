# -*- coding: utf-8 -*-
"""
Homeworks - Question 5
"""
import cv2
from matplotlib import pyplot as plt
import numpy as np
import math

# --- read image ---
img_orig = cv2.imread('./imagesHW/hw5_insurance_form.JPG')
img = cv2.cvtColor(img_orig, cv2.COLOR_BGR2RGB)
img_gray = cv2.cvtColor(img_orig, cv2.COLOR_BGR2GRAY)


# --- first do edge detection ---
edges = cv2.Canny(img_gray, 50, 150, apertureSize = 3)


# --- get lines using hough transform ---
lines = cv2.HoughLines(edges, 1, np.pi / 180, 255, None, 0, 0) # 255 / 600

# create a copy of the image to draw the found lines onto
img_copy = img.copy()

# draw each line on the copied image
if lines is not None:
    for i in range(0, len(lines)):
        rho = lines[i][0][0]
        theta = lines[i][0][1]
        a = math.cos(theta)
        b = math.sin(theta)
        x0 = a * rho
        y0 = b * rho
        pt1 = (int(x0 + 2000*(-b)), int(y0 + 2000*(a)))
        pt2 = (int(x0 - 2000*(-b)), int(y0 - 2000*(a)))
        cv2.line(img_copy, pt1, pt2, (0,0,255), 3, cv2.LINE_AA)


plt.imshow(img_copy, cmap="gray"); plt.axis('off'); plt.title('Detected lines using Hough transform'); 
plt.show()


# --- calculate rotation ---
# calculate the minimal difference of the line angle and either a direction of 0°, 1/2 pi, pi and 3/2 pi
# take this angle difference and rotate the image by that angle. the lines should be now a multiple of 1/2 pi -> vertical or horizontal

# the four directions
dirs = [(np.pi / 2) * i for i in range(4)]
min_diffs = []

# iterate over all lines and store the minimal difference to the nearest of the four directions
for i in range(0, len(lines)):
    theta = lines[i][0][1]
    diffs = [abs(theta - angle) for angle in dirs]

    min_diff = np.min(diffs)
    min_diffs.append(min_diff)
# take the median element of the resulting list, that way outlining angles get ignored
median_diff = np.median(min_diffs)

# now rotate the image with this value
image_center = tuple(np.array(img.shape[1::-1]) / 2)
rot_mat = cv2.getRotationMatrix2D(image_center, np.rad2deg(median_diff), 1.0)
rotated = cv2.warpAffine(img_gray, rot_mat, img.shape[1::-1], flags=cv2.INTER_LINEAR)
# crop away the black area that appeared after rotation
rotated = rotated[40:-40, 40:-40]


# draw the result
fig, axs = plt.subplots(1, 2)
fig.set_figheight(10.80); fig.set_figwidth(19.20)
axs[0].imshow(img_gray, cmap='gray'); axs[0].set_title('Original'); axs[0].axis('off')
axs[1].imshow(rotated, cmap='gray'); axs[1].set_title('Rotated image'); axs[1].axis('off')

plt.show()

# --------------------------------------------------------------------
# --- now we want to trim array all the whitespace around the form ---
# --------------------------------------------------------------------
# first we invert the image, that way the text will be white and the background black
inverted = 255*(rotated < 128).astype(np.uint8)

# than we can use cv2.findNonZero on the inverted image to find all text points (which are now non-zero (white))
coords = cv2.findNonZero(inverted)
# now we can get the bounding rectangle that this points spawn. we get a rectangle where all text-points are within
x, y, w, h = cv2.boundingRect(coords)

# now we can crop away everything that lies outside of our bounding rectangle, since we now that there is no text within
rotated_cropped = rotated[y-1:y+h, x:x+w]
# ------------------------------------------------------------------------------------------
# --- we use hough transform again to detect now the lines in the rotated, cropped image ---
# ------------------------------------------------------------------------------------------

# get the edges using canny again
rotated_cropped_edges = cv2.Canny(rotated_cropped, 50, 150, apertureSize = 3)
# use hough transform
lines_2 = cv2.HoughLines(rotated_cropped_edges, 1, np.pi / 180, 280, None, 0, 0)
# the resulting image
result = rotated_cropped.copy()

# again iterate over all lines and draw a line on our resulting image
# this ensures that all the gaps between the lines will be filled
if lines_2 is not None:
    for i in range(0, len(lines_2)):
        rho = lines_2[i][0][0]
        theta = lines_2[i][0][1]
        a = math.cos(theta)
        b = math.sin(theta)
        x0 = a * rho
        y0 = b * rho
        pt1 = (int(x0 + 2000*(-b)), int(y0 + 2000*(a)))
        pt2 = (int(x0 - 2000*(-b)), int(y0 - 2000*(a)))
        cv2.line(result, pt1, pt2, (0,0,255), 1, cv2.LINE_AA)
        
# draw the result
fig, axs = plt.subplots(1, 2)

fig.set_figheight(10.80)
fig.set_figwidth(19.20)
axs[0].imshow(img_gray, cmap='gray'); axs[0].set_title('Original'); axs[0].axis('off')
axs[1].imshow(result, cmap='gray'); axs[1].set_title('Resulting image: rotated, cropped and lines restored'); axs[1].axis('off')

plt.show()


# --- finally, save resulted image ---
plt.imsave('./results/question5_insurance_form_restored.jpg', result, cmap = 'gray')