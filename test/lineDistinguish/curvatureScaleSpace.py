import cv2
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
img = cv2.imread('straight.jpeg',0)
ret, binary = cv2.threshold(img,127,255,0) 
img1, contours, hierarchy = cv2.findContours(binary,1,2) 
cv2.drawContours(img1,contours,0,(0,0,255),3)
linecontours = np.vstack(contours[0]).squeeze()
#linecontours = vsplit(linecontours, 2) 
print(linecontours)
print(type(linecontours))
plt.imshow(linecontours,cmap='gray')
plt.show()
#cv2.waitKey(0)
cv2.waitKey(0)
