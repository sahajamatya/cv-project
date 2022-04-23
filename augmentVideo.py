from this import d
import cv2
import cv2.aruco as aruco
import numpy as np
import os

from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile
from tkVideoPlayer import TkinterVideo
import time
import tkinter as tk
from tkVideoPlayer import TkinterVideo


class Substitution:
    def __init__(self, sourceVideo="", destinationVideo="", outputVideo=""):
        self.sourceVideo = sourceVideo
        self.destinationVideo = destinationVideo
        self.outputVideo = outputVideo

    def findArucoMarkers(self, img, markerSize=6, totalMarkers=250, draw=True):
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkers}')
        arucoDict = aruco.Dictionary_get(key)
        arucoParam = aruco.DetectorParameters_create()
        corners, ids, rejected = aruco.detectMarkers(
            imgGray, arucoDict, parameters=arucoParam)
        # Corners: [top right, bottom right, bottim left, top left]
        return corners, ids

    def setSourceVideo(self, filename):
        self.sourceVideo = filename

    def getSourceVideo(self):
        return self.sourceVideo

    def setDestinationVideo(self, filename):
        self.destinationVideo = filename

    def getDestinationVideo(self):
        return self.destinationVideo

    def setOutputVideo(self, filename):
        self.outputVideo = filename

    def getOutputVideo(self):
        return self.outputVideo


def augment(src, dest, subs):
    video = cv2.VideoCapture(dest.split("/")[-1])
    videoAug = cv2.VideoCapture(src.split("/")[-1])
    print("=====")
    print(src.split("/")[-1], dest.split("/")[-1])
    print("=====")
    out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(
        *'MPEG'), 45, (int(video.get(3)), int(video.get(4))))
    while True:
        _, imgAug = videoAug.read()
        _, frame = video.read()
        corners, ids = subs.findArucoMarkers(frame)

        if ids is not None:
            if len(ids) > 0:
                # print(ids)
                for corner, id in zip(corners, ids):
                    if id == [0]:
                        tl = int(corner[0][0][0]), int(corner[0][0][1])
                    elif id == [1]:
                        tr = int(corner[0][1][0]), int(corner[0][1][1])
                    elif id == [2]:
                        bl = int(corner[0][3][0]), int(corner[0][3][1])
                    elif id == [3]:
                        br = int(corner[0][2][0]), int(corner[0][2][1])
                h, w, _ = imgAug.shape
                pts1 = np.array([tl, tr, br, bl])
                pts2 = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
                matrix, _ = cv2.findHomography(pts2, pts1)
                imgOut = cv2.warpPerspective(
                    imgAug, matrix, (frame.shape[1], frame.shape[0]))
                cv2.fillConvexPoly(frame, pts1.astype(int), (0, 0, 0))
                imgOut = frame + imgOut
        out.write(imgOut)
        key = cv2.waitKey(1)
        if key == 27 or key == ord('q'):
            cv2.destroyAllWindows()
            break


def main():
    window = Tk()
    subs = Substitution()
    window.title("Tkinter Play Videos in Video Player")
    window.geometry("1200x1200")
    window.configure()

    def open_file(typeOfFile):
        if typeOfFile == "output":
            augment(subs.getSourceVideo(), subs.getDestinationVideo(), subs)
            videoplayerOutput = TkinterVideo(
                master=window, scaled=True, pre_load=False)
            print(videoplayerOutput.load(r"{}".format('output.avi')))
            videoplayerOutput.place(relx=0.5, y=500, anchor=CENTER)
            videoplayerOutput.play()
        else:
            file = askopenfile(mode='r')
            if file is not None:
                global filename
                filename = file.name
                global videoplayer
                videoplayer = TkinterVideo(
                    master=window, scaled=True, pre_load=False)
                videoplayer.load(r"{}".format(filename))
                if typeOfFile == "source":
                    subs.setSourceVideo(filename)
                    videoplayer.place(x=100, y=150)
                elif typeOfFile == "dest":
                    subs.setDestinationVideo(filename)
                    videoplayer.place(x=900, y=150)
                videoplayer.play()

    lbl1 = Label(window, text="Video on Video Augmentation",
                 font="none 24 bold")
    lbl1.config(anchor=CENTER)
    lbl1.place(relx=0.5, y=20, anchor=CENTER)

    sourceBtn = Button(window, text='Select Source Video',
                       command=lambda: open_file("source"))
    sourceBtn.place(x=100, y=100)

    destBtn = Button(window, text='Select Destination Video',
                     command=lambda: open_file("dest"))
    destBtn.place(x=900, y=100)

    outputBtn = Button(window, text='Generate Output Video',
                       command=lambda: open_file("output"))
    outputBtn.place(relx=0.5, y=300, anchor=CENTER)
    window.mainloop()

    subs = Substitution()
    video = cv2.VideoCapture("frame.mov")
    videoAug = cv2.VideoCapture("falcon.mov")
    out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(
        *'MPEG'), 45, (int(video.get(3)), int(video.get(4))))
    while True:
        _, imgAug = videoAug.read()
        _, frame = video.read()
        corners, ids = subs.findArucoMarkers(frame)

        if ids is not None:
            if len(ids) > 0:
                # print(ids)
                for corner, id in zip(corners, ids):
                    if id == [0]:
                        tl = int(corner[0][0][0]), int(corner[0][0][1])
                    elif id == [1]:
                        tr = int(corner[0][1][0]), int(corner[0][1][1])
                    elif id == [2]:
                        bl = int(corner[0][3][0]), int(corner[0][3][1])
                    elif id == [3]:
                        br = int(corner[0][2][0]), int(corner[0][2][1])
                h, w, _ = imgAug.shape
                pts1 = np.array([tl, tr, br, bl])
                pts2 = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
                matrix, _ = cv2.findHomography(pts2, pts1)
                imgOut = cv2.warpPerspective(
                    imgAug, matrix, (frame.shape[1], frame.shape[0]))
                cv2.fillConvexPoly(frame, pts1.astype(int), (0, 0, 0))
                imgOut = frame + imgOut
        out.write(imgOut)
        key = cv2.waitKey(1)
        if key == 27 or key == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    main()
