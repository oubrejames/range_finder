# import the necessary packages
import numpy as np
import argparse
import cv2

# TODO: Make it a stream from the robots camera
# image = cv2.imread("red_stuff.PNG")
image = cv2.imread("2FT_FLAG_2.jpg")
image = cv2.resize(image, (720, 960))  # Resize image
cv2.imshow("imagesv", image)

# define the list of boundaries

img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

## Gen lower mask (0-5) and upper mask (175-180) of RED
mask1 = cv2.inRange(img_hsv, (0,50,20), (5,255,255))
mask2 = cv2.inRange(img_hsv, (175,50,20), (180,255,255))

## Merge the mask and crop the red regions
mask = cv2.bitwise_or(mask1, mask2 )
croped = cv2.bitwise_and(image, image, mask=mask)

## Display
cv2.imshow("mask", mask)
cv2.imshow("croped", croped)
cv2.waitKey()
