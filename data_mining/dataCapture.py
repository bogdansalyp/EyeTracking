import numpy as np
import cv2
import time
import random
import os
# from videocaptureasync import VideoCaptureAsync

BACKGROUND_COLOR = (111, 111, 111)
CIRCLE_COLOR = (255, 255, 255)

# 1280x720

# Set directory to write to, Input name of participant, maybe some training or testing datasets (no need in "/" in the end)
path = "dataDir/" + time.strftime("%d%b %H:%M:%S")
window_name = "Hello"
blankPath = "/Users/bogdansalyp/projects/EyeTracking/data_mining/blank.jpg"

# Try to create a directory, if there is no success, program will not start capturing
try:
    os.makedirs(path)
    os.chdir(path)
except OSError:
    exit()


# Start timer with capture
cnt = 1
lastTime = time.time()
spreadTime = 0 # x + 1 = Time between frame capture
cap = cv2.VideoCapture(0)
cap.set(3,320)
cap.set(4,240)

# Set the center of image
xPos = 640
yPos = 360

# Set speed of circle
xSpd = 4
ySpd = 2

# Set the start movement direction
xFlag = "right" 
yFlag = "down" 

# Text settings
font = cv2.FONT_HERSHEY_PLAIN
textPos = (10,700)
textPos2 = (1100,700)

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
    if xPos == 1280:
        xFlag = "left"
    elif xPos == 0:
        xFlag = "right"
    if yPos == 720:
        yFlag = "up"
    elif yPos == 0:
        yFlag = "down"
    return (xFlag, yFlag)

time.sleep(3)

with open("meta.txt", "w+") as f:
    f.write("frame record delay: " + str(spreadTime) + "\n")
    f.write("X speed: " + str(xSpd) + "\n")
    f.write("Y speed: " + str(ySpd) + "\n")

cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

circleImage = cv2.imread(blankPath)
# cap.start()
while True:

    # Draw a circle
    for i in range(10):
        cv2.circle(circleImage, (xPos, yPos), 10, BACKGROUND_COLOR, 10)
        xPos,  yPos  = xyChange(xPos, yPos, xSpd, ySpd)
        xFlag, yFlag = posCheck(xPos, yPos, xFlag, yFlag)
        cv2.circle(circleImage, (xPos, yPos), 10, CIRCLE_COLOR, 10)
        cv2.imshow(window_name, circleImage)

    # Write circle's position
    # '''
    # cv2.putText(circleImage, str(xPos) + " " + str(yPos), textPos, font, fontScale2, fontColorText, lineType)
    # cv2.putText(circleImage, "frame: " + str(cnt), textPos2, font, fontScale2, fontColorText, lineType)
    # '''
    # Display the resulting frame
    #cv2.imshow('frame', circleImage)

    # Quit when "q" is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    
    # Lets take one frame every second and write it to our directory
    if time.time() - lastTime <= spreadTime:
        print(time.time())
        firstTime = time.time()
        
    else:
        # Capture frame
        ret, frame = cap.read(1, )
        cnt = cnt + 1
        # Insert capture here
        pth = str(cnt) + " {" + str(xPos) + ":" + str(yPos) + "}" + ".jpg"
        faceImage = cv2.flip(cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA), 1)
        cv2.imwrite(pth, faceImage)


# When everything done, release the capture
# cap.stop()
cap.release()
cv2.destroyAllWindows()
