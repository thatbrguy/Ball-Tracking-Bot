# Ball-Tracking-Bot
A simple bot that can track a ball. Pure computer vision. No machine learning involved.

### Why no machine learning?
Sure, with the current hype, one would want to apply ML/DL. But, the simpler computer vision solution is better because:
- Higher FPS (Way higher)
- No need to train
- Works well on edge devices (Raspberry Pi)

### What does it do?
This bot was originally created to enable a drone (on a raspberry pi) to autonomously track a ball. We need to calibrate the color of the ball before we get started.

The code in this repo does not have the GPIO configuration that is used to give a feedback to the drone. Instead, it opens your webcam, and tracks the ball infront of it.

See it in action by playing `test.avi`.

### Requirements
- OpenCV
- NumPy

### Instructions
- Run `calibrate.py` and adjust the HSV values to segment out the ball. Note the HSV low and high values.
- Set the low and high values in `track.py` 
- Save it and execute `python track.py`.

