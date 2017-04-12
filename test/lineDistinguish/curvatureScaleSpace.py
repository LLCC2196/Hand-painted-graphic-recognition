import cv2
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
img = cv2.imread('Concentric2.jpeg',0)
img1 = cv2.imread('Concentric2.jpeg')
ret, binary = cv2.threshold(img,127,255,0) 
img2, contours, hierarchy = cv2.findContours(binary,1,2) 
cv2.drawContours(img1,contours,0,(0,0,255),3) 
cv2.drawContours(img1,contours,1,(255,0,0),3) 
cv2.drawContours(img1,contours,2,(0,255,0),3) 
cv2.drawContours(img1,contours,3,(0,255,255),3) 
#cv2.drawContours(img1,contours,4,(255,255,0),3) 
#cv2.drawContours(img1,contours,5,(255,0,255),3) 
#print(contours[0])
print(contours[0])
cv2.imshow("Image",img1)
cv2.waitKey(0)
dG = np.zeros(img.shape, np.uint8)  
ddG = np.zeros(img.shape, np.uint8) 
dG = cv2.Sobel(img,cv2.CV_16S, 1, 1, 3)
ddG = cv2.Sobel(img,cv2.CV_16S, 2, 2, 3)

plt.subplot(1,3,1),plt.imshow(img,cmap = 'gray')
plt.title('Original'), plt.xticks([]), plt.yticks([])
plt.subplot(1,3,2),plt.imshow(dG,cmap = 'gray')
plt.title('Sobel-1'), plt.xticks([]), plt.yticks([])
plt.subplot(1,3,3),plt.imshow(ddG,cmap = 'gray')
plt.title('Sobel-2'), plt.xticks([]), plt.yticks([])

plt.show()
