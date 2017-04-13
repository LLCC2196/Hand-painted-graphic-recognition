import cv2
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
img = cv2.imread('line3.jpeg',0)
img1 = cv2.imread('line3.jpeg')
ret, binary = cv2.threshold(img,127,255,0) 
img2, contours, hierarchy = cv2.findContours(binary,1,2) 
cv2.drawContours(img1,contours,0,(0,0,255),2) 
#cv2.drawContours(img1,contours,4,(255,255,0),3) 
#cv2.drawContours(img1,contours,5,(255,0,255),3) 
print(contours[0])
cnt = contours[0]
#cv2.waitKey(0)
cv2.imshow("Image",img1)
cv2.waitKey(0)
