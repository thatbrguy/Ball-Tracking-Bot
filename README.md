# Ball-Tracking-Bot
A simple bot that can track a ball in three dimensions, using a 2D video input. No machine learning involved.

<p align="center">
  <img src="/test.gif" alt="Ball-Tracking-Bot in action">
 </p>

### Features
This bot uses pure computer vision concepts. Compared to conventional ML models, it:
- Has a higher FPS.
- Has a lower computational complexity. (Works well on edge devices like the Raspberry Pi)
- Need not be trained.

### What does it do?
This bot was originally created to enable a drone (on a raspberry pi) to autonomously track a ball in all three dimensions. A brief note on the working is given below:

- We need to calibrate a HSV threshold such that we can mask out our target ball.
- Once a mask is created, we perform a couple of erosions and dilations to remove noise.
- The largest contour in the mask is identified. The centre and radius of the smallest circle that can enclose this contour is calculated.
- By comparing the centre value with the camera's midpoint, we can detect motion in the XY direction.
- By comparing the radius value with the guide rectangles (on our image), we can detect motion in the Z direction.

The code in this repo does not have the GPIO configuration that is used to give a feedback to the drone. Instead, it opens your webcam, and tracks the ball infront of it.

See it in action by playing `test.avi`.

### Requirements
- OpenCV
- NumPy

### Instructions
- Run `calibrate.py` and adjust the HSV values to segment out the ball. Note the HSV low (HL,SL,VL) and HSV high (HH,SH,VH) values.
- Execute `python track.py --hsv_low HL,SL,VL --hsv_high HH,SH,VH`.
- Optionally, you can modify the options --offset_x and --offset_y to adjust sensitivity.

### References
- [PyImageSearch](https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/)
