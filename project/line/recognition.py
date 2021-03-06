#Created on: May 23, 2017
#Author: chen
#llcc2196@gmail.com
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
import pandas as pd
import math
import cv2
import os  
import csv
import sys
import getopt
#get_ipython().magic('matplotlib inline')


# In[124]:

#sort the lines(horizon,vertical,left diagonal,right diagonal)
def lines_sort(degree,tolerance_h = 10,tolerance_v = 10,
        tolerance_l = 10,tolerance_r = 10):
    if(((90 - tolerance_h) <= degree and degree <= 90) or
       (-90 <= degree and degree <= (-90 + tolerance_h))):
        linesort = 'vertical'
        bias = (tolerance_v - abs(abs(degree) - 90))/tolerance_v
    elif((0 - tolerance_h) <= degree and degree <= (0 + tolerance_h)): 
        linesort = 'horizon'
        bias = (tolerance_h - abs(degree))/tolerance_h
    elif((-45 - tolerance_h) <= degree and degree <= (-45 + tolerance_h)):
        linesort = 'right diagonal'
        bias = abs(abs(degree) - 45)
    elif((45 - tolerance_h) <= degree and degree <= (45 + tolerance_h)):
        linesort = 'left diagonal'
        bias = (tolerance_l - abs(abs(degree) - 45))/tolerance_l
    else: 
        linesort = 'incorrect'
        bias = 0
    return linesort,bias


# In[125]:

#cutoff should equal to the width of line
def lineContours(img,cutoff = 5):
    ret, binary = cv2.threshold(img,127,255,0) 
    img2, contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE) 
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


# In[126]:

def lineContinuity(contournumber):
    return 1/(contournumber-1)


# In[127]:

def lineSmooth(ddline,threshold = 60):
    aveddline = np.array(ddline)
    smooth = [elem for elem in aveddline if elem < threshold]
    smooth = [elem for elem in aveddline if elem > -threshold]
    return np.var(smooth)


# In[128]:

#img should be the image only have one approximate line
#tolerance_* is the degree bias(0~45) of the line compared to the correct line
#_h-horizon _v-vertical _l-left diagonal r-right diagonal
def lineDistinguish(img,tolerance_h = 10,tolerance_v = 10,
       tolerance_l = 10,tolerance_r = 10):
    cnt,connum = lineContours(img)

    [vx,vy,x,y] = cv2.fitLine(cnt, cv2.DIST_HUBER,0,0.01,0.01)
    line_radian = math.atan(vy/vx)
    line_degree = line_radian / math.pi * 180
    return (lines_sort(line_degree,tolerance_h,tolerance_v,
            tolerance_l,tolerance_r))
    '''
    #show image with fitline
    rows,cols = img.shape[:2]
    lefty = int((-x*vy/vx) + y)
    righty = int(((cols-x)*vy/vx)+y)
    cv2.line(img,(cols-1,righty),(0,lefty),(0,255,0),2)
    cv2.imshow('Image',img)
    cv2.waitKey(0)
    '''


# In[129]:

def lineSize(lineType,contour,suitable = 0.65,x_axis = 1000,y_axis = 1000):
    if lineType == 'vertical':
        return len(contour)/(suitable*y_axis)
    elif lineType == 'horizon':
        return len(contour)/(suitable*x_axis)
    else :
        return len(contour)/(suitable*((x_axis**2+y_axis**2)**0.5))


# In[130]:

def derivativeX(point1,point2):
    dpointx = float(point2[0] - point1[0]) 
    return dpointx


# In[131]:

def derivativeY(point1,point2):
    dpointy = float(point2[1] - point1[1])
    return dpointy


# In[132]:

def derivative(point1,point2):
    dpoint = float((point2[1] - point1[1]) / (point2[0] - point1[0])) 
    if math.isinf(dpoint) :
        dpoint = 50
    return dpoint


# In[133]:

def lineDerivativeX(line,step=1,averstep=1):
    dlinex = []
    for i in range(0,len(line)-averstep,step):
        dlinex.append(derivativeX(line[i],line[i + averstep]))
    return dlinex


# In[134]:

def lineDerivativeY(line,step=1,averstep=1):
    dliney = []
    for i in range(0,len(line)-averstep,step):
        dliney.append(derivativeY(line[i],line[i + averstep]))
    return dliney


# In[135]:

def lineDerivative(line,step=1,averstep=1):
    dline = []
    for i in range(0,len(line)-averstep,step):
        dline.append(derivative(line[i],line[i + averstep]))
    return dline


# In[136]:

def lineCurvatureX(dline,step=1,averstep=1):
    ddlinex = []
    for i in range(0,len(dline)-averstep,step):
        ddlinex.append(dline[i+averstep] - dline[i])
    return ddlinex


# In[137]:

def lineCurvatureY(dline,step=1,averstep=1):
    ddliney = []
    for i in range(0,len(dline)-averstep,step):
        ddliney.append(dline[i+averstep] - dline[i])
    return ddliney


# In[138]:

def lineCurvature(dline,step=1,averstep=1):
    ddline = []
    for i in range(0,len(dline)-averstep,step):
        ddline.append(dline[i+averstep] - dline[i])
    return ddline


# In[139]:

def lineProperty(img,dstep=1,daverstep=1,ddstep=1,ddaverstep=1):
    linesort,bias = lineDistinguish(img)
    contour,connum = lineContours(img)
    Size = lineSize(linesort,contour)
    Continuity = lineContinuity(connum)
    dline = lineDerivative(contour,dstep,daverstep)
    ddline = lineCurvature(dline,ddstep,ddaverstep)
    Smooth = lineSmooth(ddline)
    return linesort,bias,Size,Continuity,Smooth


# In[140]:

#plot the line properties(original image,line,derivative of line,curvature of line),x_axis,y_axis is image size
def plotLineproperties(img,contour,dline,ddline,amplitude = 10,x_axis = 1000,y_axis = 1000):

    plt.figure(figsize=(15,15))
    plt.subplot(2,2,1),plt.title('original image')
    plt.imshow(img)
    
    x = contour[:,0]
    y = contour[:,1]
    plt.figure(figsize=(15,15))
    plt.subplot(2,2,2),plt.title('contour points')
    plt.plot(x,y),plt.axis([0, x_axis, 0, y_axis])

    td = np.arange(0, len(dline))
    plt.figure(figsize=(15,15))
    plt.subplot(2,2,3),plt.plot(td,dline),plt.title('contour derivative'),plt.axis([0, len(dline), -amplitude, amplitude])

    tdd = np.arange(0, len(ddline))
    plt.figure(figsize=(15,15))
    plt.subplot(2,2,4),plt.plot(tdd,ddline),plt.title('contour curvature'),plt.axis([0, len(ddline), -amplitude, amplitude])
    plt.show()


# In[147]:

def WriteCSVFileName(IMAGEPATH,OUTCSVPATH,OUTCSVNAME):
    with open(OUTCSVPATH+OUTCSVNAME,'w',encoding='utf8',newline='') as f:                 #w is erase, a+ is append
        writer = csv.writer(f)
        writer.writerow(["ip", "usrname", "type", "date", "num","fullname","Sort",
                         "Bias","Size","Continuity","Smooth"])
        for root, dirs, files in os.walk(IMAGEPATH):  
            for file in files:  
                splitname = os.path.splitext(file)
                if splitname[1] == '.jpeg': 
                    name = splitname[0].split("_")
                    name.append(file)
                    writer.writerow(name)                    
    f.close()
#def ReadCSVFileName(csvfilePATH)


# In[193]:

def WriteLogtxt(LOGPATH,ITEM,linesort,bias,Size,Continuity,Smooth):
    with open(LOGPATH + ITEM +'.txt','ab+') as logtxt: 
        logtxt.seek(-3,2)
        if (str(logtxt.read())[-4:-1] == 'END'):
            logtxt.close()
        else:
            logtxt.close()
            with open(LOGPATH + ITEM +'.txt','a+') as log:
                log.write(',Sort:' + linesort)
                log.write(',Bias:' + bias)
                log.write(',Size:' + Size)
                log.write(',Continuity:' + Continuity)
                log.write(',Smooth:' + Smooth)
                log.write(',END')
            log.close()


# In[213]:

def LinePropertiesAddCSVandLOG(IMAGENAME,OUTCSVPATH,OUTCSVNAME,LOGPATH):
    if IMAGENAME[-5:] == '.jpeg':
        img = cv2.imread(IMAGEPATH+IMAGENAME,0)
        linesort,bias,Size,Continuity,Smooth = lineProperty(img,1,10)
        with open(OUTCSVPATH+OUTCSVNAME,'a+',encoding='utf8',newline='') as f: #w is erase, a+ is append
            writer = csv.writer(f)
            name = IMAGENAME[:-5].split("_")
            name.append(IMAGENAME)
            name.append(linesort)
            name.append(bias)
            name.append(Size)
            name.append(Continuity)
            name.append(Smooth)
            writer.writerow(name)
        f.close()
        #add csv line        
        WriteLogtxt(LOGPATH,IMAGENAME[:-5],linesort,str(bias),str(Size),str(Continuity),str(Smooth))
        #write log
        print('name:',IMAGENAME)
        print('Type:',linesort)
        print('degree accuracy:',bias)
        print("line size:%.3f"%Size)
        print("continuity:%.3f"%Continuity)
        print("smooth:%.3f"%Smooth)
        #print properties
    else: print('Not a jpeg image\n')
#def ReadCSVFileName(csvfilePATH)


# In[163]:

def linePropertiesWriteCSVandLOG(img,imagecsv,linename):
        linesort,bias,Size,Continuity,Smooth = lineProperty(img,1,10)
        imagecsv.loc[imagecsv["fullname"]==linename, 'Sort'] = linesort
        imagecsv.loc[imagecsv["fullname"]==linename, 'Bias'] = bias
        imagecsv.loc[imagecsv["fullname"]==linename, 'Size'] = Size
        imagecsv.loc[imagecsv["fullname"]==linename, 'Continuity'] = Continuity
        imagecsv.loc[imagecsv["fullname"]==linename, 'Smooth'] = Smooth
        WriteLogtxt(LOGPATH,linename[:-5],linesort,str(bias),str(Size),str(Continuity),str(Smooth))
        '''
        print(linecsvlist[0])
        print('name:',line)
        print('Type:',linesort)
        print('degree accuracy:',bias)
        print("line size:%.3f"%Size)
        print("continuity:%.3f"%Continuity)
        print("smooth:%.3f"%Smooth)
        '''
#plotLineproperties(imgori,contour,dline,ddline,60)

def getargv(argv):
    IMAGEPATH = ''
    LOGPATH = ''
    OUTCSVPATH = ''
    IMAGENAME = ''
    OUTCSVNAME = ''
    try:
        opts, args = getopt.getopt(argv,"hi:l:o:n:c:",["IMAGEPATH=","LOGPATH=","OUTCSVPATH=","IMAGENAME=","OUTCSVNAME="])
    except getopt.GetoptError:
        print('test.py -i <IMAGEPATH> -l <LOGPATH> -o <OUTCSVPATH> -n <IMAGENAME> -c <OUTCSVNAME>')
        print('e.g: #test.py -i ./image/ -l ./image/ -o ./image/ -n 32.212.54.126_qwer_Line_2017-05-19-09-18-33_6786.jpeg -c batchoutput.csv')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('test.py -imgp <IMAGEPATH> -logp <LOGPATH> -outp <OUTCSVPATH> -imgn <IMAGENAME> -outn <OUTCSVNAME>')
            sys.exit()
        elif opt in ("-i", "--IMAGEPATH"):
            IMAGEPATH = arg
        elif opt in ("-l", "--LOGPATH"):
            LOGPATH = arg
        elif opt in ("-o", "--OUTCSVPATH"):
            OUTCSVPATH = arg
        elif opt in ("-n", "--IMAGENAME"):
            IMAGENAME = arg
        elif opt in ("-c", "--OUTCSVNAME"):
            OUTCSVNAME = arg
    return IMAGEPATH,LOGPATH,OUTCSVPATH,IMAGENAME,OUTCSVNAME


#******************************************************************run**********************************************************************************#

#$~:python3.4 recognition.py -i ./image/ -l ./image/ -o ./image/ -n 32.212.54.126_qwer_Line_2017-05-19-09-18-33_6786.jpeg -c batchoutput.csv
IMAGEPATH,LOGPATH,OUTCSVPATH,IMAGENAME,OUTCSVNAME = getargv(sys.argv[1:])

#calculate exist image into batchoutput.csv and write to logtxt(use linePropertiesWriteCSVandLOG)
'''
WriteCSVFileName(IMAGEPATH,OUTCSVPATH,OUTCSVNAME)
imagecsv = pd.read_csv(OUTCSVPATH+OUTCSVNAME)
linepd = imagecsv[imagecsv["type"]=='Line'] #select line
linepd = linepd.sort_index(by=['date','num'],ascending=True).reset_index() #sorting as save time
linefullname = linepd['fullname']
for line in linefullname: 
    img = cv2.imread(IMAGEPATH+line,0)
#   imgori = cv2.imread(IMAGEPATH+line)
    linePropertiesWriteCSVandLOG(img,imagecsv,line) 
imagecsv.to_csv(OUTCSVPATH+OUTCSVNAME,index=False)
'''
#add a new image into ./image/ called '32.212.54.126_qwer_Line_2017-05-19-09-18-33_6786.jpeg'

#calculate new image  add into batchoutput.csv and write to its logtxt(use LinePropertiesAddCSVandLOG)
if IMAGENAME[-35:-29] == '_Line_':
    LinePropertiesAddCSVandLOG(IMAGENAME,OUTCSVPATH,OUTCSVNAME,LOGPATH)




