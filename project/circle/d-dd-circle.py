#Created on: Apr 18, 2017
#Author: chen
#llcc2196@gmail.com
import cv2
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
import math

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
def derivative(point1,point2):
	dpoint = float((point2[1] - point1[1]) / (point2[0] - point1[0])) 
	if math.isinf(dpoint) :
		dpoint = 50
	return dpoint

def lineDerivative(line,step=1,averstep=1):
	dline = []
	for i in range(0,len(line)-averstep,step):
		dline.append(derivative(line[i],line[i + averstep]))
	return dline	

def lineCurvature(dline,step=1,averstep=1):
	ddline = []
	for i in range(0,len(dline)-averstep,step):
		ddline.append(dline[i+averstep] - dline[i])
	return ddline	

#plot the line properties(original image,line,derivative of line,curvature of line),x_axis,y_axis is image size
def plotLineproperties(img,contour,dline,ddline,amplitude = 10,x_axis = 400,y_axis = 400):

	plt.subplot(2,2,1),plt.title('original image')
	plt.imshow(img)

	x = contour[5:,0]
	y = contour[5:,1]
	plt.subplot(2,2,2),plt.title('contour points')
	plt.plot(x,y),plt.axis([0, x_axis, 0, y_axis])
	
	td = np.arange(0, len(dline))
	plt.subplot(2,2,3),plt.plot(td,dline),plt.title('contour derivative'),plt.axis([0, len(dline), -amplitude, amplitude])

	tdd = np.arange(0, len(ddline))
	plt.subplot(2,2,4),plt.plot(tdd,ddline),plt.title('contour curvature'),plt.axis([0, len(ddline), -amplitude, amplitude])
	plt.show()
	return 0

img = cv2.imread('circle3-1000.jpeg',0)
imgori = cv2.imread('circle3-1000.jpeg')
contour = lineContours(img)
dline = lineDerivative(contour,1,10)
ddline = lineCurvature(dline)
plotLineproperties(imgori,contour,dline,ddline,60,1000,1000)


#cv2.waitKey(0)


