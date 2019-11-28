import numpy as np
import cv2
import time
import random
import os

# Set directory to write to, Input name of participant, maybe some training or testing datasets (no need in "/" in the end)
path = "/Users/olegserebrennikov/Documents/Prog/videoCapture/"
dirName = input() + "/" + time.strftime("%d%b %H:%M")

# Try to create a directory, if there is no success, program will not start capturing
try:
    os.makedirs(path + dirName)
    os.chdir(path + dirName)
except OSError:
    exit()


# Start timer with capture
cnt = 1
zeroSec = time.strftime("%s")
firstSec = time.strftime("%s")
spreadSec = 2 # x + 1 = Time between frame capture
cap = cv2.VideoCapture(0)

# Set the center of image
xPos = 640
yPos = 360

# Set speed of circle
xSpd = 20
ySpd = 10

# Set the start movement direction
xFlag = "right" 
yFlag = "down" 

# Text settings
font = cv2.FONT_HERSHEY_PLAIN
textPos = (10,700)
fontScale1 = 2
fontScale2 = 1
fontColorText = (255,255,255)
fontColorDVD = (0,0,255)
lineType = 2
dvdText = "CMEPTb"

# Change coordinates of Dot
def xyChange(xPos, yPos, xSpd, ySpd):
    if xFlag == "right":
        xPos = xPos + xSpd
    elif xFlag == "left":
        xPos = xPos - xSpd
    if yFlag == "down":
        yPos = yPos + ySpd
    elif yFlag == "up":
        yPos = yPos - ySpd
    return xPos, yPos
    
# Change directions when touching window sides
def posCheck(xPos, yPos, xFlag, yFlag):

    # Set the corners for specific text/geometry
    if xPos == 1160:
        xFlag = "left"
    elif xPos == 0:
        xFlag = "right"
    if yPos == 720:
        yFlag = "up"
    elif yPos == 20:
        yFlag = "down"
    return (xFlag, yFlag)

time.sleep(3)

with open("meta.txt", "w+") as f:
    f.write("frame record delay: " + str(spreadSec) + "\n")
    f.write("X speed: " + str(xSpd) + "\n")
    f.write("Y speed: " + str(ySpd) + "\n")


while True:
    
    # Capture frame-by-frame
    ret, frame = cap.read(1,)

    rgbImage = cv2.flip(cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA), 1)
    newImage = rgbImage

    # Draw a circle
    cv2.circle(rgbImage, (xPos, yPos), 10, (0, 0, 255), 10)
    
    # Draw a DVD label
    #cv2.putText(rgbImage, dvdText, (xPos, yPos), font, fontScale1, fontColorDVD, lineType)
    
    # Refresh coordinates
    xPos,  yPos  = xyChange(xPos, yPos, xSpd, ySpd)
    xFlag, yFlag = posCheck(xPos, yPos, xFlag, yFlag)

    # Write circle's position
    cv2.putText(rgbImage, str(xPos) + " " + str(yPos), textPos, font, fontScale2, fontColorText, lineType)

    # Display the resulting frame
    cv2.imshow('frame', rgbImage)

    # Quit when "q" is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    
    # Lets take one frame every second and write it to our directory
    if int(firstSec) - int(zeroSec) <= spreadSec:
        firstSec = time.strftime("%s")
    else:
        cnt = cnt + 1
        # Insert capture here
        pth = str(cnt) + " {" + str(xPos) + ":" + str(yPos) + "}" + ".jpg"
        cv2.imwrite(pth, newImage)
        zeroSec = firstSec


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

