import cv2
import numpy as np


def lineContours(img):
	ret, binary = cv2.threshold(img,127,255,0) 
	img2, contours, hierarchy = cv2.findContours			(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE) 
#If you pass cv2.CHAIN_APPROX_NONE, all the boundary points are stored.
	linecontours = np.vstack(contours[2]).squeeze()
	'''
	if len(linecontours) % 2 != 0:
		linecontours = linecontours[:-1]
	contour = np.vsplit(linecontours, 2) 
	'''
	return linecontours

img1 = cv2.imread('circle2-1000.jpeg',0)
img2 = cv2.imread('circle3-1000.jpeg',0)
img3 = cv2.imread('circle4-1000.jpeg',0)
img4 = cv2.imread('circle6-1000.jpeg',0)

ret, thresh = cv2.threshold(img1, 127, 255,0)
ret, thresh2 = cv2.threshold(img2, 127, 255,0)

cnt1 = lineContours(img1)
cnt2 = lineContours(img2)
cnt3 = lineContours(img3)
cnt4 = lineContours(img4)

ret1 = cv2.matchShapes(cnt1,cnt2,1,0.0)
ret2 = cv2.matchShapes(cnt1,cnt3,1,0.0)
ret3 = cv2.matchShapes(cnt1,cnt4,1,0.0)
print(' ',ret1,' ',ret2,' ',ret3)
