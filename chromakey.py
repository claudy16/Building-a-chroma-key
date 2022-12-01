import cv2
import numpy as np
import sys

#To be able to read any video and files that we ask terminal to modify
cap = cv2.VideoCapture(sys.argv[1])
_, frame = cap.read()
#modify background by its file format
bg = str(sys.argv[2])
filename = bg[len(bg)-3:len(bg)]
if filename == "mp4" or filename == "avi":
    bck = cv2.VideoCapture(sys.argv[2])
else:
    bck = cv2.imread(sys.argv[2])
    i = cv2.resize(bck,dsize=(frame.shape[1],frame.shape[0]))




#Saving our chroma video in mp4 format
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(sys.argv[3],fourcc, 10, (frame.shape[1],frame.shape[0]))

while(1):
    # Take each frame
    _, frame = cap.read()

    if filename == "mp4" or filename == "avi":
        _, bframe = bck.read()
        i = cv2.resize(bframe,dsize=(frame.shape[1],frame.shape[0]))

        
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([65,30,120])
    upper_blue = np.array([80,170,255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)

    background = cv2.bitwise_and(i, i,mask=mask.astype(np.uint8))
    croma = frame.copy()
    croma = cv2.bitwise_and(croma, croma, mask=(np.bitwise_not(mask)).astype(np.uint8))
    canvas = croma + background 

    out.write(canvas)

    #cv2.imshow('frame',frame)
    #cv2.imshow('mask',mask)
    cv2.imshow('canvas',canvas)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
out.release()
    
# Closes all the frames
cv2.destroyAllWindows()
   
print("The video was successfully saved")
