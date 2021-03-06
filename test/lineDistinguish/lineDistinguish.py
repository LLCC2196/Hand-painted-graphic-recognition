#Created on: Apr 8, 2017
#Author: chen
#llcc2196@gmail.com
import cv2
import numpy as np
import math

img = cv2.imread('line4.jpeg',0)
#sort the lines(horizon,vertical,left diagonal,right diagonal)
def lines_sort(degree,tolerance_h = 10,tolerance_v = 10,
		tolerance_l = 10,tolerance_r = 10):
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
	ret,thresh = cv2.threshold(img,127,255,0)
	im2,contours,hierarchy = cv2.findContours(thresh, 1, 2)
	cnt = contours[0]

	[vx,vy,x,y] = cv2.fitLine(cnt, cv2.DIST_HUBER,0,0.01,0.01)
	line_radian = math.atan(vy/vx)
	line_degree = line_radian / math.pi * 180
	print(lines_sort(line_degree,tolerance_h,tolerance_v,
			tolerance_l,tolerance_r))

	rows,cols = img.shape[:2]
	lefty = int((-x*vy/vx) + y)
	righty = int(((cols-x)*vy/vx)+y)
	cv2.line(img,(cols-1,righty),(0,lefty),(0,255,0),2)
	cv2.imshow("Image", img)
	cv2.waitKey(0)

lineDistinguish(img)
