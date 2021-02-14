# -*- coding: utf-8 -*-
"""
Homeworks - Question 3 (b)
"""
import cv2
import numpy as np
from matplotlib import pyplot as plt
import math
import time

# --- loading the images ---
img1_orig = cv2.imread('./imagesHW/hw3_building.jpg')
img2_orig = cv2.imread('./imagesHW/hw3_train.jpg')

img1_gray = cv2.cvtColor(img1_orig, cv2.COLOR_BGR2GRAY)
img2_gray = cv2.cvtColor(img2_orig, cv2.COLOR_BGR2GRAY)

# --- specifying the weights ---
weights = [[0, 1, 1, 1, 0],
           [1, 2, 2, 2, 1],
           [1, 2, 4, 2, 1],
           [1, 2, 2, 2, 1],
           [0, 1, 1, 1, 0]]
# convert the simple python list to an numpy list, that way we can access properties like array.shape easily
weights = np.asarray(weights)

# ------------------------------
# --- weighted median filter ---
# ------------------------------

def weighted_median_position(img, x, y, kernel):
    """Calculates the weighted median for the given pixel as position (x, y) of the image 'img' with the weights 'kernel'."""
    # the list we store all the values in to later calculate the median
    median_list = []
    
    kernel_width_halfed = math.floor(kernel.shape[0] / 2)
    kernel_height_halfed = math.floor(kernel.shape[1] / 2)
    
    for ky in range(kernel.shape[1]):
        for kx in range(kernel.shape[0]):
            # we need coordinates relative to the kernel center (i.e. for kernel size (5, 5) the values will be between -2 and +2)
            dx = kx - kernel_width_halfed
            dy = ky - kernel_height_halfed
            
            # the current position in the image
            curr_pos = (x + dx, y + dy)
            
            # check if we are within image boundaries
            # we decided to introduce no additional border around the image for the sliding window
            # we simply only add pixels to the median list, if we are withing boundaries
            if curr_pos[0] < 0 or curr_pos[0] >= img.shape[0]:
                continue
            if curr_pos[1] < 0 or curr_pos[1] >= img.shape[1]:
                continue
            
            # get the current pixel value at the current position
            curr_pixel_value = img[curr_pos[0], curr_pos[1]]
            # get the current weight of the current kernel position
            curr_weight = kernel[kx, ky]
            
            # add the current pixel value n-times to the median-list, where n is the current weight
            for w in range(curr_weight):
                median_list.append(curr_pixel_value)
        
    median_value = np.median(median_list)
    # round it to the next integer value (since we are using values of 0-255 for pixel data)
    median_value = int(np.round(median_value))
    
    return median_value


def weighted_median(img, weights):
    # the matrix we store the filtered image in
    result = np.zeros(img.shape)
    # iterate over each pixel in the image and calculate the weighted median for this position
    for y in range(img.shape[1]):
        for x in range(img.shape[0]):
            # fill the resulting image with the median filtered data
            result[x][y] = weighted_median_position(img, x, y, weights)
    
    return result


# -------------------------------------------------------
# --- apply the weighted median to our example images ---
# -------------------------------------------------------

# caution: the calculation of the weighted median takes a long time (~20s for the first image on my cpu)
# there are a lot of nested for-loops that are hard to replace with faster operations
print('Caution: the calculation of the weighted median takes a long time (~27s for the first image on my cpu)')
print('...there are a lot of nested for-loops that are hard to replace with faster operations')

start_time_img1 = time.time()
img1_w_median = weighted_median(img1_gray, weights)
print("Image 1 took: --- %s seconds ---" % (time.time() - start_time_img1))

start_time_img2 = time.time()
img2_w_median = weighted_median(img2_gray, weights)
print("Image 2 took: --- %s seconds ---" % (time.time() - start_time_img2))

# store the results
plt.imsave('./results/question3/hw3_building_weighted_median.jpg', img1_w_median, cmap = 'gray')
plt.imsave('./results/question3/hw3_train_weighted_median.jpg', img2_w_median, cmap = 'gray')

# plot the results of part (a) and part (b)
# (code from part (a)):
median13 = cv2.medianBlur(img1_gray,3)
median23 = cv2.medianBlur(img2_gray,3)

median15 = cv2.medianBlur(img1_gray,5)
median25 = cv2.medianBlur(img2_gray,5)

fig = plt.figure(figsize=(19.20,10.80))
plt.subplot(231),plt.imshow(median13, cmap='gray'), plt.title('Median1 (3x3)')
plt.subplot(232),plt.imshow(median15, cmap='gray'), plt.title('Median2 (5x5)')
plt.subplot(233),plt.imshow(img1_w_median, cmap='gray'), plt.title('Weighted median1')

plt.subplot(234),plt.imshow(median23, cmap='gray'), plt.title('Median1 (3x3)')
plt.subplot(235),plt.imshow(median25, cmap='gray'), plt.title('Median2 (5x5)')
plt.subplot(236),plt.imshow(img2_w_median, cmap='gray'), plt.title('Weighted median2')
plt.show()


# -----------------------------
# --- comparing the results ---
# -----------------------------

# The weighted median seems to outperform the "normal" median with a (3x3) kernel performed in part (a) in noise reduction pretty consistently.
# The noise reduction seems to be at least as good as the median filter with a (5x5) kernel.
# What stands out though is, that the weighted median preserves sharp edges and features way better.
# This can be seen especially good at the fence in the foreground or the stoop of the house.
# So it seems that weighted median filtering outperforms the "normal" variants in both areas, at the cost of being more computation-intensive
# (and most likely given, the right weights are used).