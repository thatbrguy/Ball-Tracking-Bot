import os
import cv2
import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add('--hsv_low', help='Comma separated HSV LOW values after calibration', default='0,48,176')
parser.add('--hsv_high', help='Comma separated HSV HIGH values after calibration', default='17,255,255')
parser.add('--offset_x', help='Sensitivity in the X direction (in pixels)', default='0')
parser.add('--offset_y', help='Sensitivity in the Y direction (in pixels)', default='0')
args = parser.parse_args()

OUTPUT_PATH = os.path.join(os.getcwd(), 'Output')
HSV_LOW = [int(i) for i in args.hsv_low.split(',')]
HSV_HIGH = [int(i) for i in args.hsv_high.split(',')]

if __name__ == '__main__':

    def rectangle_values(frame_center, frame_xy, factor):

        top_left = int((frame_xy[0] / factor) * 1.4)
        top_right = int((frame_xy[1] / factor) * 1.4)
        bottom_left = 2*frame_center[0] - top_left
        bottom_right = 2*frame_center[1] - top_right

        return top_left, top_right, bottom_left, bottom_right

    # Creating output folder if it doesn't exist
    if not os.path.exists(OUTPUT_PATH):
        os.mkdir(OUTPUT_PATH)

    # Capture video from the stream
    cap = cv2.VideoCapture(0)

    frame_center = (320, 240)
    frame_xy = (640, 480)
    offset_x = int(args.offset_x)
    offset_y = int(args.offset_y)
    count = 0

    while(1):

        _, frame=cap.read()
     
        # convert from a BGR stream to an HSV stream
        hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Enter the calibrated values in the below function. 
        # Replace (0, 48, 176) by  new LOW values and (17, 255, 255) by new HIGH values.

        mask = cv2.inRange(hsv, HSV_LOW, HSV_HIGH) 
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2) 

        contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        string = ''

        # Guide rectangles
        cv2.circle(frame, frame_center, 5, (255, 255, 255), -1)
        top_leftx, top_lefty, bottom_rightx, bottom_righty = rectangle_values(frame_center, frame_xy, factor = 2.3 * 2)
        breadth_small = frame_xy[1] - 2 * top_lefty
        cv2.rectangle(frame, (top_leftx, top_lefty), (bottom_rightx, bottom_righty), (255, 255, 255), 3)

        top_leftx, top_lefty, bottom_rightx, bottom_righty = rectangle_values(frame_center, frame_xy, factor = 3.5 * 2)
        breadth_large = frame_xy[1] - 2 * top_lefty
        cv2.rectangle(frame, (top_leftx, top_lefty), (bottom_rightx, bottom_righty), (255, 255, 255), 3)

        # only proceed if at least one contour was found
        if len(contours) > 0:

            # Finding the largest contour
            c = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            
            # (x,y) are the coordinates of the circle's center
            # We only proceed further if the radius is greater than 10

            if radius > 10:
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 0, 255), 2)
                cv2.circle(frame, (int(x),int(y)), 5, (0, 255, 0), -1)

                # Movement calculations
                offset_x = frame_center[0] - x
                offset_y = frame_center[1] - y

                # Here, we set a threshold displacement of 20
                if(abs(offset_x) > 20):
                    if(offset_x < 0):
                        string += 'RIGHT '
                    elif(offset_x > 0):
                        string += 'LEFT '

                if(abs(offset_y) > 20):
                    if(offset_y < 0):
                        string += 'UP '
                    elif(offset_y > 0):
                        string += 'DOWN '

                # Move front/back wrt ball's diameter
                if(2 * radius > breadth_large):
                    string += 'BACK '
                elif(2 * radius < breadth_small):
                    string += 'FRONT '

        cv2.putText(frame, string, (10,450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 215, 255), 2, cv2.LINE_AA)

        cv2.imshow('Track', frame)
        cv2.imwrite(os.path.join(OUTPUT_PATH, str(count) + '.jpg'), frame)
        count += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()