import cv2
import numpy as np
import ttkbootstrap as ttk

def getFrame(frame_nr):
    global cap
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_nr)


def draw_on_frame(event, x, y, flags, param):
    global drawing, last_x, last_y, c_x, c_y

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        last_x, last_y = x, y
        c_x, c_y = x,y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            c_x,c_y = x,y
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        c_x,c_y = x,y

drawing = False
last_x, last_y = -1, -1
c_x, c_y = -1,-1

cap = cv2.VideoCapture("01-Fuggveny.mp4")
ret, frame = cap.read()

nr_of_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))


cv2.namedWindow("Video Player")
cv2.createTrackbar('Frame','Video Player',0,nr_of_frames,getFrame)
cv2.setMouseCallback("Video Player", draw_on_frame)

while cap.isOpened():
    if ret:
        cv2.rectangle(frame, (last_x,last_y), (c_x,c_y), (0,255,0),2)
        cv2.imshow("Video Player", frame)
        cv2.setTrackbarPos("Frame","Video Player",int(cap.get(cv2.CAP_PROP_POS_FRAMES)))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        ret, frame = cap.read()
    else:
        break

cap.release()
cv2.destroyAllWindows()





