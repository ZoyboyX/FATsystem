import time
import cv2
import keyboard
import numpy as np

def run():
    start = time.perf_counter_ns()
    capture = cv2.VideoCapture(0)
    time.sleep(1)
    imagearray = []
    timearray = []
    width = int(capture.get(3))
    height = int(capture.get(4))
    size = (width, height)
    outfile = cv2.VideoWriter("outfile.avi", cv2.VideoWriter_fourcc('M', 'J', 'P','G'),30, size)
    while(capture.isOpened()):
        val, frame = capture.read()
        cv2.waitKey(1)
        outfile.write(frame)
        #cv2.imshow('vidio', frame)
        if(keyboard.is_pressed('r')):
            break

    capture.release()
    outfile.release()
    cv2.destroyAllWindows()

    toprocess = cv2.VideoCapture('outfile.avi')
    framecount = int(toprocess.get(cv2.CAP_PROP_FRAME_COUNT))
    finalimage = np.zeros((height,framecount,3), np.uint8)
    middle = int(width/2)
    for x in range(0, framecount-1):
        val, frame = toprocess.read()
        cv2.waitKey(1)
        for y in range(0,height):
            blue = frame[y,middle,0]
            green = frame[y,middle,1]
            red = frame[y,middle,2]
            finalimage[y,x] = [blue, green, red]
    cv2.imwrite("final.png", finalimage)




