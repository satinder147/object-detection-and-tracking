# HELLO EVERYBODY I AM SATINDER SINGH, A ENGINEERING STUDENT ARMY INSTITUTE OF TECHNOLOGY PUNE, I AM COMPUTER SCIENCE STUDENT
# THIS IS A SMALL PROJECT ABOUT COMPUTER VISION USING OPEN CV AND PYTHON
#IN THIS PROJECT I TRACK A SPECIFIC COLOR AND DRAW LINES
#HOPE YOU LIKE IT
#YOU CAN ALSO WATCH A DEMONSTRATION ON MY YOUTUBE CHANNEL reactor science DON'T FORGET TO LIKE SUBSCRIBE AND SHARE


#Importing desired python libraries
import numpy as np
import cv2


#creating a empty python list
l=[]


#making a cap variable for the video feed "0" represents the primary camera, you can choose any other also by specifying it's number
cap=cv2.VideoCapture(0)


#starting a infinte loop for recording the video
while(1):
#capturing video frame by frame in frame
    
    ret,frame=cap.read()
#converting the video to HSV because it is easy to detect colors in HSV image
    
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
#creating boundary for color range
    
    lower=np.array([100,50,50])
    upper=np.array([135,255,255])
#creating a mask .i.e whatever lies in the specified color range is converted to white and rest is converted to black you can uncomment the next line to see the mask
    
#cv2.imshow('mask',mask)
    
    mask=cv2.inRange(hsv,lower,upper)
#as there is noise in the image first the image is eroded and then dilated to remove the noise
    
    mask=cv2.erode(mask,None,iterations=2)
    mask=cv2.dilate(mask,None,iterations=2)
#blur is added to remove further noise
    
    mask=cv2.GaussianBlur(mask,(5,5),0)
#and operation is applied between frame and mask
#as the mask contains white(.i.e 1 where the specified color is detected) else there is black
#the original image is colored means if you account for every pixel every pixel has value more than or equal to 1 so if we do and operation of voth the images
#we get only the required region and rest other is black
#you can uncomment the next line to see the mask
#cv2.imshow('masked',masked)
    
    masked=cv2.bitwise_and(frame,frame,mask=mask)
#as for contour detection image required has to be in GRAY so converting masked to gray
    
    nmasked=cv2.cvtColor(masked,cv2.COLOR_BGR2GRAY)
#detecting the contours
    
    img,contours,heirarchy=cv2.findContours(nmasked,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#making varialbes
    
    m_area=0
    ci=0
#if length of contours is greater than zero
    
    if(len(contours)>0):
#iterating through the contours, I want to find the contour with maximum area and ignoring others
        
        for i in range(len(contours)):
            cnt=contours[i]
#finding area of the present contour
            
            area=cv2.contourArea(cnt)
#if area is greater than the m_area then storing the present index (that is the value of "i")
            
            if(area>m_area):
                a=i
                m_area=area
#selecting the contours with the maximum area
                
        cnt=contours[a]
#fiding moments
        
        m=cv2.moments(cnt)
#this is a common error comers in which m['m00']becomes 0 thus creating problems in the divsions ahead
        
        if(m['m00']!=0):
#finding the centroid of the contour
            
            x1=int(m['m10']/m['m00'])
            y1=int(m['m01']/m['m00'])
#drawing a red dot,(-1 fill the circle) at the centroid of the contour
            
            cv2.circle(frame,(x1,y1),6,(0,0,255),-1,cv2.LINE_AA)
            center=(x1,y1)
#inserting the centroid in the list
            l.append(center)
            
            if(len(l)>1):
    
#lets draw the lines for the tracking
                for i in range(1,len(l)):
                    cv2.line(frame,l[i-1],l[i],(0,255,0),2,cv2.LINE_AA)
 #if length of line increases by 50 then i start removing the elements from the beginging
                    
                if(len(l)>50):
                    del l[0]
            
#i draw a enclosing circle for the contour
                    
        (x,y),r=cv2.minEnclosingCircle(cnt)
        center=(int(x),int(y))
        r=int(r)
        cv2.circle(frame,center,r,(255,0,0),2,cv2.LINE_AA)
        cv2.drawContours(frame,cnt,-1,(0,255,0),2)
# as the video i receive from my webcam is laterally inversed i flip it
        
    frame=cv2.flip(frame,1)
# i show the frame
    
    cv2.imshow('frame',frame)
# if 'q' is pressed then exit the program
    
    if(cv2.waitKey(1)&0XFF==ord('q')):
        break
# releaasing the cap
cap.release()
#destroying all the windows
cv2.destroyAllWindows()
    
