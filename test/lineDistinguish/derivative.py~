import cv2
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
def derivative(point1,point2):
	dpoint = (point2[1] - point1[1]) / (point2[0] - point1[0]) 
	return dpoint
def lineDerivative(line):
	dline = np.zeros(len(line)-1)
	for i in range(len(line)-1):
		dline[i] = derivative(line[i],line[i + 1])
	return dline	
def lineCurvature(line):
	dline = lineDerivative(line)
	ddline = np.zeros(len(dline)-1)
	for i in range(len(dline)-1):
		ddline[i] = dline[i+1] - dline[i]
	return ddline	
line = np.array( [ (1,1), (2,2), (3,3), (4,4) ] )
ddline = lineCurvature(line)
print(ddline)

cv2.waitKey(0)

