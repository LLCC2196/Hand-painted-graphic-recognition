import cv2
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
img = cv2.imread('circle2-1000*1000.jpeg',0)
img1 = cv2.imread('circle2-1000*1000.jpeg')
ret, binary = cv2.threshold(img,127,255,0) 
img2, contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE) 
cv2.drawContours(img1,contours,1,(0,0,255),2) 
#cv2.drawContours(img1,contours,4,(255,255,0),3) 
#cv2.drawContours(img1,contours,5,(255,0,255),3) 
linecontours = np.vstack(contours[1]).squeeze()
#contour = np.vsplit(linecontours, 2)
if len(linecontours) % 2 != 0:
	linecontours = linecontours[:-1]
#print(len(linecontours))
cnt = linecontours
#cv2.waitKey(0)
cv2.imshow("Image",img1)
cv2.waitKey(0)
