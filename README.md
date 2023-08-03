# Eye Blink Detection with Live Plot

Detect eye blinks in real-time using facial landmarks and visualize the blink rate on a live plot. The script captures video from your webcam and processes it to count the number of blinks.

## Prerequisites

Make sure you have Python and the required libraries installed:

```bash
pip install opencv-python
pip install cvzone
```

## About the Script

The script uses the FaceMeshDetector from the cvzone library to detect facial landmarks, specifically focusing on the right eye. It calculates the ratio between vertical and horizontal distances of certain landmarks to determine if an eye blink has occurred. The blink rate is plotted on a live graph using the LivePlot module.

The script continuously monitors your blinks while displaying the webcam feed. Press the spacebar to exit the program.
