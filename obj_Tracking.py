import numpy as np
import cv2
import sys

video_path = 'testVid.mp4'
cv2.ocl.setUseOpenCL(False)
    
version = cv2.__version__.split('.')[0]
print (version) 

#read video file
cap = cv2.VideoCapture(video_path)

#check opencv version
if version == '2' :
	fgbg = cv2.BackgroundSubtractorMOG2()
if version == '3': 
	fgbg = cv2.createBackgroundSubtractorMOG2()

ret,frame = cap.read()
#region = cv2.selectROI(frame,False)
region = cv2.selectROI(frame,True,False)
print(region)
(xx,yy,ww,hh)=region

#Destroy the selected window
cv2.destroyAllWindows()
counter = 0
font = cv2.FONT_HERSHEY_SIMPLEX

while (cap.isOpened):

	#if ret is true than no error with cap.isOpened
	ret, frame = cap.read()
	
	if ret==True:

		#apply background substraction
		fgmask = fgbg.apply(frame)
					
		#check opencv version
		if version == '2' : 
			(contours, hierarchy) = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		if version == '3' : 
			(im2, contours, hierarchy) = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		
		#looping for contours
		for c in contours:
			if cv2.contourArea(c) < 500:
				continue
				
			#get bounding box from countour
			(x, y, w, h) = cv2.boundingRect(c)
			
			#draw bounding box
			if(y+int(h/2) >= yy+int(hh/2)-2 and y+int(h/2) <= yy+int(hh/2)+2):
				counter = counter+1
				print(counter)
				cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
			else:
				cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		
		cv2.line(frame,(xx,yy+int(hh/2)),(xx+ww,yy+int(hh/2)),(0,0,255),2) 	
		cv2.putText(frame,'Counter:'+str(counter),(0,30),font,0.8,(255,255,255),2,cv2.LINE_AA)
		cv2.imshow('foreground and background',fgmask)
		cv2.imshow('rgb',frame)
		#if cv2.waitKey(1) & 0xFF == ord("q"):
		#	break
		k = cv2.waitKey(40) & 0xff
		if (k == 37):
			break

cap.release()
cv2.destroyAllWindows()
