#Created on: Apr 8, 2017
#Author: chen
#llcc2196@gmail.com
import cv2
import numpy as np
import math


#cutoff should equal to the width of line
def lineContours(img,cutoff = 5):
	ret, binary = cv2.threshold(img,127,255,0) 
	img2, contours, hierarchy = cv2.findContours			(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE) 
#If you pass cv2.CHAIN_APPROX_NONE, all the boundary points are stored.
	for i in range(1,len(contours)):
		linecontours = np.vstack(contours[i]).squeeze()
		if len(linecontours) % 2 != 0:
			linecontours = linecontours[:-1]
		contour = np.vsplit(linecontours, 2) 
		if(i == 1):
			con = contour[0][cutoff:-cutoff]
		else:
			con = np.vstack((contour[0][cutoff:-cutoff],con))
	return con,len(contours)
#sort the lines(horizon,vertical,left diagonal,right diagonal)
def lines_sort(degree,tolerance_h = 10,tolerance_v = 10,
		tolerance_l = 10,tolerance_r = 10):
	print(degree)
	if(((90 - tolerance_h) <= degree and degree <= 90) or
	   (-90 <= degree and degree <= (-90 + tolerance_h))):
		linesort = 'vertical'
	elif((0 - tolerance_h) <= degree and degree <= (0 + tolerance_h)): 
		linesort = 'horizon'
	elif((-45 - tolerance_h) <= degree and degree <= (-45 + tolerance_h)):
		linesort = 'right diagonal'
	elif((45 - tolerance_h) <= degree and degree <= (45 + tolerance_h)):
		linesort = 'left diagonal'
	else: linesort = 'incorrect'
	
	return linesort	
#img should be the image only have one approximate line
#tolerance_* is the degree bias(0~45) of the line compared to the correct line
#_h-horizon _v-vertical _l-left diagonal r-right diagonal
def lineDistinguish(img,tolerance_h = 10,tolerance_v = 10,
		   tolerance_l = 10,tolerance_r = 10):
	cnt,cntnum = lineContours(img)

	[vx,vy,x,y] = cv2.fitLine(cnt, cv2.DIST_HUBER,0,0.01,0.01)
	line_radian = math.atan(vy/vx)
	line_degree = line_radian / math.pi * 180
	print(lines_sort(line_degree,tolerance_h,tolerance_v,
			tolerance_l,tolerance_r))

	rows,cols = img.shape[:2]
	lefty = int((-x*vy/vx) + y)
	righty = int(((cols-x)*vy/vx)+y)
	cv2.line(img,(cols-1,righty),(0,lefty),(0,255,0),2)
	cv2.imshow('Image',img)
	cv2.waitKey(0)

img1 = cv2.imread('line4-1000.jpeg',0)
img2 = cv2.imread('line5-1000.jpeg',0)
img3 = cv2.imread('line6-1000.jpeg',0)
img4 = cv2.imread('line7-1000.jpeg',0)
lineDistinguish(img1)
lineDistinguish(img2)
lineDistinguish(img3)
lineDistinguish(img4)

