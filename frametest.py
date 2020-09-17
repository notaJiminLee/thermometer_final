import cv2

#cap = cv2.VideoCapture('/dev/video0')

#cap = cv2.VideoCapture('v4l2src device=/dev/video0 ! image/jpeg, width=1920, height=1080, framerate=30/1 ! jpegparse ! jpegdec ! videoconvert ! videoscale ! appsink sync=false', cv2.CAP_GSTREAMER)
#cap = cv2.VideoCapture("nvarguscamerasrc ! 'video/x-raw(memory:NVMM),width=800, height=600, framerate=30/1, format=NV12' ! nvvidconv flip-method=0 ! 'video/x-raw,width=800, height=600, format=BGRx' ! videoconvert ! video/x-raw, format=BGR ! appsink", cv2.CAP_GSTREAMER)
#cap = cv2.VideoCapture('nvarguscamerasrc ! video/x-raw, width=1920, height=1080, format=I420, framerate=30/1 ! nvvidconv flip-method=2 ! video/x-raw, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink', cv2.CAP_GSTREAMER)
#cap = cv2.VideoCapture("nvarguscamerasrc ! video/x-raw,width=1920, height=1080, framerate=30/1, format=NV12, framerate=30/1 ! nvvidconv flip-method=2 ! video/x-raw, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink", cv2.CAP_GSTREAMER)
cap = cv2.VideoCapture('nvarguscamerasrc ! video/x-raw(memory:NVMM), width=1280, height=720, format=NV12, framerate=30/1 ! nvvidconv ! video/x-raw, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink', cv2.CAP_GSTREAMER)


if cap.isOpened():
    print('width: {}, height: {}'.format(cap.get(3), cap.get(4)))
else:
    exit()
while True:
    ret, frame = cap.read()

    if ret:
        cv2.imshow('video', frame)
        cv2.waitKey(1)
        
cap.release()
cv2.destroyAllWindows()
