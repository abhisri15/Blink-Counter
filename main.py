import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot

cap = cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces=1)
plotY = LivePlot(540, 220, [20, 50], invert=True)

# width and height for the window
window_width = 1080
window_height = 440

# window name
window_name = "Image"

cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

# Resize the window to desired dimensions
cv2.resizeWindow(window_name, window_width, window_height)

idList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]
ratioList = []
blinkCounter = 0
counter = 0
color = (255, 0, 255)

# rather than taking just the distance between extreme upper/lower or left/right it's better if we take ratio since it
# normalizes it

while True:
    # Suppose you have a video playing rather than webCam
    # use the following code to play the video on loop, the momemt fps reached threshold, it restarts again

    # if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
    #     cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        face = faces[0]
        for id in idList:
            cv2.circle(img, face[id], 5, color, cv2.FILLED)

        rightUp = face[159]
        rightDown = face[23]
        rightLeft = face[130]
        rightRight = face[243]

        lengthVer, _ = detector.findDistance(rightUp, rightDown)
        lengthHor, _ = detector.findDistance(rightLeft, rightRight)

        cv2.line(img, rightUp, rightDown, (0, 255, 0), 3)
        cv2.line(img, rightLeft, rightRight, (0, 255, 0), 3)

        ratio = int((lengthVer / lengthHor) * 100)
        ratioList.append(ratio)
        if len(ratioList) > 3:
            ratioList.pop(0)

        ratioAvg = sum(ratioList) / len(ratioList)

        if ratioAvg < 35 and counter == 0:
            blinkCounter += 1
            color = (0,200,0)
            counter = 1
        if counter != 0:
            counter += 1
            if counter > 10:
                counter = 0
                color = (255,0,255)


        cvzone.putTextRect(img, f'Blink Count: {blinkCounter}', (20, 40), colorR=color)

        imgPlot = plotY.update(ratioAvg, color)
        imgPlot = cv2.resize(imgPlot, (img.shape[1], img.shape[0]))
        imgStack = cvzone.stackImages([img, imgPlot], 2, 1)

    else:
        imgStack = cvzone.stackImages([img, imgPlot], 2, 1)

    img = cv2.flip(img, 1)
    cv2.imshow(window_name, imgStack)

    if cv2.waitKey(1) == ord(' '):
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()
