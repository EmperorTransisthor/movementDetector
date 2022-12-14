from picamera.array import PiRGBArray 
from picamera import PiCamera 
import time 
import cv2 
import numpy as np 
 
camera = PiCamera()
 
camera.resolution = (640, 480)
camera.framerate = 30
raw_capture = PiRGBArray(camera, size=(640, 480))
 

back_sub = cv2.createBackgroundSubtractorMOG2(history=150, varThreshold=25, detectShadows=True)

time.sleep(0.1)
 
kernel = np.ones((20,20),np.uint8)
start = time.time()
 

for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):

    image = frame.array
 
    fg_mask = back_sub.apply(image)   
    fg_mask = cv2.morphologyEx(fg_mask,cv2.MORPH_CLOSE,kernel)
    fg_mask = cv2.medianBlur(fg_mask,5)
       
    _, fg_mask = cv2.threshold(fg_mask, 127, 255, cv2.THRESH_BINARY)
 
    contours, hierarchy = cv2.findContours(fg_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[-2:]
    areas = [cv2.contourArea(c) for c in contours]

    if len(areas) < 1:
  
      cv2.imshow('Frame',image)
      
      key = cv2.waitKey(1) & 0xFF
      raw_capture.truncate(0)
    
      if key == ord("q"):
        break
     
      continue
  
    else:
         
      max_index = np.argmax(areas)
       

    cnt = contours[max_index]
    x,y,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),3)
          
    cv2.imshow("Frame",image)
    
    moment = time.time()
    time_lapsed = moment-start
    
    if time_lapsed>60:
        start = time.time()
        timestr = time.strftime("%Y%m%d-%H%M%S")
        name = 'Capture-'+ timestr +'.jpg'
        cv2.imwrite(name,image, params = (cv2.IMWRITE_JPEG_QUALITY, 50))
     
    key = cv2.waitKey(1) & 0xFF 
    raw_capture.truncate(0)


    if key == ord("q"):
      break
 
cv2.destroyAllWindows()
