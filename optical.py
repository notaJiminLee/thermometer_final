import numpy as np
import cv2
cap = cv2.VideoCapture("nvarguscamerasrc ! video/x-raw(memory:NVMM), width=1280, height=720, format=NV12, framerate=30/1 ! nvvidconv ! video/x-raw, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink", cv2.CAP_GSTREAMER)
# params for ShiTomasi corner detection
feature_params = dict( maxCorners = 1,
                       qualityLevel = 0.01,
                       minDistance = 30,
                       blockSize = 14)
# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (15,15),
                  maxLevel = 0,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
# Create some random colors
color = np.random.randint(0,255,(100,3))
# Take first frame and find corners in it
ret, old_frame = cap.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
vis2 = np.zeros_like(old_frame)
vis2 = cv2.cvtColor(vis2, cv2.COLOR_BGR2GRAY)
pts = np.array([[0, 0],[500, 0],[500, 500],[0, 500]], np.int32)
ptsback = np.array([[0, 0],[1279, 0],[1279, 719],[0, 719]], np.int32)
vis2 = cv2.fillPoly(vis2, [ptsback], 0)
vis2 = cv2.fillPoly(vis2, [pts], 255)
vis2 = vis2.astype(np.uint8)
p0 = cv2.goodFeaturesToTrack(old_gray, mask = vis2, **feature_params)

# Create a mask image for drawing purposes
mask = np.zeros_like(old_frame)
while(1):
    ret,frame = cap.read()
    if not ret:
        break
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # calculate optical flow
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
    # Select good points
    if st > 0:
        good_new = p1[st==1]
        good_old = p0[st==1]

    # draw the tracks
    for i,(new,old) in enumerate(zip(good_new,good_old)):
        a,b = new.ravel()
        c,d = old.ravel()
        mask = cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
        frame = cv2.circle(frame,(a,b),5,color[i].tolist(),-1)
    img = cv2.add(frame,mask)
    cv2.imshow('frame',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    # Now update the previous frame and previous points
    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1,1,2)
cv2.destroyAllWindows()
