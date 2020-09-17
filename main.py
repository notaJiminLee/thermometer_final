
from threading import Thread
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
import itertools

import cv2
import time
import os
from subprocess import call
import requests

from ir import IRThread
from vis import GPUThread

from ir.utils import overlay_bboxes as overlay_ir_bboxes 
from vis.utils import draw_boxes as overlay_vis_bboxes 

def exit_handler():
    print("exit handler called")
    gpu_thread.stop()
    gpu_thread.join()
    
    cv2.destroyAllWindows()

def save_img(url):
    wtime = time.strftime('%y%m%d%H%M%S', time.localtime(time.time()))
    cv2.imwrite(os.path.join('./image', wtime + '.jpg'), vis_frame_w_overlay)
    files={'file':open('./image/' + wtime + '.jpg', 'rb')}
    r=requests.post(url, files=files, params={'temp':'36.5', 'webpath':'http://34.64.149.18:5051/images/' + wtime + '.jpg'})

if __name__ == "__main__":
    
    MAIN_MIN_LATENCY = 1/20 # run main thread at ~20Hz

    DISPLAY = True
    WIN_SIZE = (800, 600)
    FACE_BB_COLOR = (255, 255, 255) # white
    EYES_BB_COLOR = (0,   255, 255) # yellow
    LOG_DIR = "logs"

    APP_NAME = "AI Thermometer"
    VIS_WIN_NAME = APP_NAME + ": VIS frame"  # window name


    gpu_thread = GPUThread(frame_size=WIN_SIZE)
    gpu_thread.start()  # get vis frame start

    executor = ThreadPoolExecutor(max_workers=4)

    cv2.namedWindow(VIS_WIN_NAME)  # create window

    url='http://34.64.149.18:5051/upload'
    nodetecting = 0
    saveflag = 0

    try:
        while gpu_thread.frame is None:  # can't get vis frame
            print("Waiting for RGB frames")
            time.sleep(1)

        # main loop
        for i in itertools.count(start=0, step=1):
            

            time_start = time.monotonic()

	    # face detection and create bbox
            vis_frame_w_overlay, x1 = overlay_vis_bboxes(gpu_thread.frame, gpu_thread.detections)

            if x1 == 0:
                nodetecting += 1
                print(nodetecting)
                if nodetecting > 50:
                    saveflag = 1
            else:
                nodetecting = 0
                
            # Show
            cv2.imshow(VIS_WIN_NAME, vis_frame_w_overlay)

            key = cv2.waitKey(1) & 0xFF

            # Save frames
            # if the `q` key was pressed in the cv2 window, break from the loop
	    # if the 's' key was pressed in the cv2 window, save iamges and save datas to mysql DB
            if key == ord("q"):
                break
            if saveflag == 1 and nodetecting == 0:
                save_img(url)
                saveflag = 0
            main_latency =  time.monotonic() - time_start
            
            time.sleep(max(0, MAIN_MIN_LATENCY - main_latency))

    finally:
        exit_handler()
