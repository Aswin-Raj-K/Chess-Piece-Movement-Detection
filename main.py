import math
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from math import inf, floor
import modules as m
from chessBoard import ChessBoard
import os

video_file = r'Video' + os.sep + 'Video_Org.mp4'
video = []
cap = cv.VideoCapture(video_file)
ret, frame = cap.read()
refFrame = frame

# reading all frames
M, N, _ = np.shape(refFrame)

areaThreshold = 200000
thresh = m.getBlob(cv.resize(cv.cvtColor(frame, cv.COLOR_BGR2GRAY), (int(N * 0.5), int(M * 0.5))))
contours, hierarchy = cv.findContours(thresh, 1, 2)
boundary = m.getContour(contours, areaThreshold, True)[0]
refA = cv.contourArea(boundary)
boundary = m.getCorners(boundary)
intersections, edgePoints = m.getIntersections(boundary)


while ret:
    video.append(cv.resize(cv.cvtColor(frame, cv.COLOR_BGR2GRAY), (int(N * 0.5), int(M * 0.5))))
    ret, frame = cap.read()
cap.release()

frameCount = len(video)
# Finding the stable frames in the video for movement detection
stableFrames = m.findStableFrames(video, refA, areaThreshold)
print("=============================")
print("Stable Frame No:", stableFrames)
print("=============================")

chessboard = ChessBoard()

frameNo = 0
i = 0
virtualChessboard = chessboard.getBoardImage()
while True:
    orgFrame = video[frameNo]
    if i < len(stableFrames) - 1:
        if frameNo == stableFrames[i + 1]:
            virtualChessboard = m.detectMovementAndUpdateBoard(video[stableFrames[i]], video[stableFrames[i + 1]],intersections,chessboard)
            i = i + 1
    cv.imshow('Original', orgFrame)
    cv.imshow('Virtual', virtualChessboard)

    cv.waitKey(30)
    frameNo += 1
    if not frameNo < frameCount:
        break
