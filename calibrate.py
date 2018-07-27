import cv2
import numpy as np

#'optional' argument is required for trackbar creation parameters
def nothing(dummy):
    pass

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    cv2.namedWindow('Colorbars') 
     
    #assign strings for ease of coding
    hh='Hue High'
    hl='Hue Low'
    sh='Saturation High'
    sl='Saturation Low'
    vh='Value High'
    vl='Value Low'
    wnd = 'Colorbars'
    #Begin Creating trackbars for each
    cv2.createTrackbar(hl, wnd,0,179,nothing)
    cv2.createTrackbar(hh, wnd,0,179,nothing)
    cv2.createTrackbar(sl, wnd,0,255,nothing)
    cv2.createTrackbar(sh, wnd,0,255,nothing)
    cv2.createTrackbar(vl, wnd,0,255,nothing)
    cv2.createTrackbar(vh, wnd,0,255,nothing)

    while(1):
        #read the streamed frames (we previously named this cap)
        _, frame=cap.read()
     
        #convert from a BGR stream to an HSV stream
        hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #read trackbar positions for each trackbar
        hul=cv2.getTrackbarPos(hl, wnd)
        huh=cv2.getTrackbarPos(hh, wnd)
        sal=cv2.getTrackbarPos(sl, wnd)
        sah=cv2.getTrackbarPos(sh, wnd)
        val=cv2.getTrackbarPos(vl, wnd)
        vah=cv2.getTrackbarPos(vh, wnd)

        #make array for final values
        HSVLOW=np.array([hul,sal,val])
        HSVHIGH=np.array([huh,sah,vah])

        mask = cv2.inRange(hsv, HSVLOW, HSVHIGH)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        res = cv2.bitwise_and(frame, frame, mask =mask)
        cv2.imshow(wnd, res) 

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()