# -*- coding: utf-8 -*-
"""
Homeworks - Question 4
"""
# read the image
img= cv2.imread('./imagesHW/hw3_road_sign_school_blurry.JPG',0)

# copy the image to perform the transformations
im = img.copy()

# figure out how large the image is
height, width = im.shape[:2]

# select the kernel that is used for dilation-erosion
W = cv2.getStructuringElement(cv2.MORPH_CROSS,(5,5))

# apply the given algorithm
for i in range(10):
    im_d = cv2.dilate(im,W) # first dilate
    im_e = cv2.erode(im,W)  # then erode
    im_h = cv2.addWeighted(im_d,0.5,im_e,0.5,0) # then add images
    # for every pixel perform the following test
    for x in range(0,height):
        for y in range(0,width):
            pixel = im[x,y] # current pixel
            if pixel > im_h[x,y]:
                pixel = im_d[x,y]
            else:
                pixel = im_e[x,y]
    
# plot results
fig = plt.figure(figsize=(19.20,10.80))
plt.subplot(121),plt.imshow(img,cmap='gray'), plt.title('Original')
plt.subplot(122),plt.imshow(im,cmap='gray'), plt.title('Edited')
plt.show()

# save resulting image
plt.imsave('./results/question_4_road_sign_school_blurry_filtered.jpg', im, cmap = 'gray')
