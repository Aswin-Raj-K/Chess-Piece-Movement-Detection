import math
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from math import inf, floor
import modules as m
from chessBoard import ChessBoard
import os

if __name__ == "__main__":
    video_file = r'Video' + os.sep + 'Video_Org.mp4'
    video = []
    cap = cv.VideoCapture(video_file)
    ret, frame = cap.read()
    refFrame = frame

    M, N, _ = np.shape(refFrame)

    areaThreshold = 200000 #Threshold area of the contour for detecting chess board boundary
    #Gaussion, canny, dilation and thresholding
    thresh = m.getBlob(cv.resize(cv.cvtColor(frame, cv.COLOR_BGR2GRAY), (int(N * 0.5), int(M * 0.5))))
    contours, hierarchy = cv.findContours(thresh, 1, 2)
    #Finding the boundary
    boundary = m.getContour(contours, areaThreshold, True)[0]
    refA = cv.contourArea(boundary)
    #Approximating the contour to quadilateral
    boundary = m.getCorners(boundary)
    intersections, edgePoints = m.getIntersections(boundary)

    # Reading all the frames
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

    # Creating a chess board object
    chessboard = ChessBoard()

    i = frameNo = 0
    # reading the initial chessboard image
    virtualChessboard = chessboard.getBoardImage()
    isFirstFrame = True
    while True:
        orgFrame = video[frameNo]
        if i < len(stableFrames) - 1:
            if frameNo == stableFrames[i + 1]:
                # Detecting movement and updating the chess board
                virtualChessboard = m.detectMovementAndUpdateBoard(video[stableFrames[i]], video[stableFrames[i + 1]],
                                                                   intersections, chessboard)
                i = i + 1

        # displaying frames
        cv.imshow('Original', orgFrame)
        cv.imshow('Virtual', virtualChessboard)

        cv.waitKey(30)
        frameNo += 1
        if not frameNo < frameCount:
            break

        if isFirstFrame:
            cv.waitKey(30000*2)
            isFirstFrame = False
