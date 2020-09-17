import numpy as np
import cv2
import busio
import adafruit_amg88xx
import board

def thercam():
    i2c_bus=busio.I2C(board.SCL, board.SDA)
    amg = adafruit_amg88xx.AMG88XX(i2c_bus, addr=0x69)
    return amg

amg = thercam()
nowtemp = 0

def avdegree(x1, y1, x2, y2, amg):
    centerx = int((x1+x2)/2)
    centery = int((y1+y2)/2) - int((y1+y2)/2/3)
    adax = int(8/1280*centerx)
    aday = int(8/720*centery)
    if adax-1 >= 0 and adax+1 < 8 and aday-1 >= 0 and aday < 8:
        tempis = amg.pixels[adax][aday]
        return tempis, centerx, centery
    else:
        return 0, 0, 0

def draw_boxes(arr, detections):
    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0
   
    if detections is None:
        return arr, x1

    h, w = arr.shape[:2]
    scores = detections[:,2]
    
    # loop over the detections
    for (_, _, score, x1, y1, x2, y2) in detections[scores > 0.5]:
        # scale box
        box = np.array([x1, y1, x2, y2]) * np.array([w, h, w, h])
        
        # cast to int
        (x1, y1, x2, y2) = box.astype("int")
        
        # draw box
        cv2.rectangle(arr, (x1, y1), (x2, y2),(0, 0, 255), 2)  

        global nowtemp
        nowtemp, centerx, centery = avdegree(x1, y1, x2, y2, amg)
        if nowtemp > 0: 
            cv2.circle(arr, (centerx, centery) , int(3), (int(0),int(255),int(0)), int(-1))

        # put text
        cv2.putText(
            arr,
            f"{nowtemp:.2f}",
            (x1, y1 - 10 if y1 > 20 else y1 + 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (0, 0, 255),
            2
        )


    return arr, x1
