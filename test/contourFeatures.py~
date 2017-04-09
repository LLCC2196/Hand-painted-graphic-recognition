import cv2
import numpy as np
img = cv2.imread('star.jpg',0)
ret,thresh = cv2.threshold(img,127,255,0)
im2,contours,hierarchy = cv2.findContours(thresh, 1, 2)
cnt = contours[0]
M = cv2.moments(cnt)
ret,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)
th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)
cv2.imshow("Image", img)
cv2.imshow("thresh", thresh)
cv2.imshow("th1", th1)
cv2.imshow("th2", th2)
cv2.imshow("th3", th3)
#阈值
cv2.waitKey(0)
#计算质心
print(M)
cx = int(M['m10']/M['m00'])
cy = int(M['m01']/M['m00'])
print("cx:")
print(cx)
print("cy:")
print(cy)
#轮廓面积
area = cv2.contourArea(cnt)
print("area:")
print(area)
#轮廓周长
perimeter = cv2.arcLength(cnt,True)
print("perimeter:")
print(perimeter)
#轮廓近似
epsilon = 0.1*cv2.arcLength(cnt,True)
approx = cv2.approxPolyDP(cnt,epsilon,True)#2D点
#凸函数
hull = cv2.convexHull(cnt)
#检测凹凸性a function to check if a curve is convex or not
k = cv2.isContourConvex(cnt)
print(k)
#边界矩形
x,y,w,h = cv2.boundingRect(cnt)
cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
cv2.imshow("Image1", img)
cv2.waitKey(0)
img = cv2.imread('star.jpg',0)
rect = cv2.minAreaRect(cnt)
box = cv2.boxPoints(rect)
box = np.int0(box)
cv2.drawContours(img,[box],0,(0,0,255),2)
cv2.imshow("Image2", img)
cv2.waitKey(0)
img = cv2.imread('star.jpg',0)
(x,y),radius = cv2.minEnclosingCircle(cnt)
center = (int(x),int(y))
radius = int(radius)
cv2.circle(img,center,radius,(0,255,0),2)
cv2.imshow("Image3", img)
cv2.waitKey(0)
img = cv2.imread('star.jpg',0)
ellipse = cv2.fitEllipse(cnt)
cv2.ellipse(img,ellipse,(0,255,0),2)
cv2.imshow("Image4", img)
cv2.waitKey(0)
img = cv2.imread('star.jpg',0)
rows,cols = img.shape[:2]
[vx,vy,x,y] = cv2.fitLine(cnt, cv2.DIST_L2,0,0.01,0.01)
lefty = int((-x*vy/vx) + y)
righty = int(((cols-x)*vy/vx)+y)
cv2.line(img,(cols-1,righty),(0,lefty),(0,255,0),2)
cv2.imshow("Image5", img)
cv2.waitKey(0)
