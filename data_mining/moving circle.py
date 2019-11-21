import numpy as np
import cv2
import time
import random

start_time = time.time()
cap = cv2.VideoCapture(0)

#задаем центр кадра
x = 640
y = 360
flag = 0

#задаем количество времени записи
#while (time.time() - start_time) < 20: 
while True:
    if x > 1280:
        flag = 1
    elif x < 0:
        flag = 0
    
    if flag == 0:
        x = x + 20
    if flag == 1:
        x = x - 20

    tim = int(time.time() - start_time)
    # Capture frame-by-frame
    ret, frame = cap.read()

    cv2.circle(frame, (x, y), 10, (255,255,255), 100)
    
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGBA)

    # Display the resulting frame
    cv2.imshow('frame',gray)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    
        
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
