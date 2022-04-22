import cv2
import cv2.aruco as aruco
import numpy as np
import os


def findArucoMarkers(img, markerSize=6, totalMarkers=250, draw=True):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkers}')
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()
    corners, ids, rejected = aruco.detectMarkers(
        imgGray, arucoDict, parameters=arucoParam)
    # Corners: [top right, bottom right, bottim left, top left]
    return corners, ids


def augmentAruco(corner, id, img, imgAug):
    # print(id, "\n")
    tl = corner[0][0][0], corner[0][0][1]
    tr = corner[0][1][0], corner[0][1][1]
    br = corner[0][2][0], corner[0][2][1]
    bl = corner[0][3][0], corner[0][3][1]

    h, w, c = imgAug.shape

    pts1 = np.array([tl, tr, br, bl])
    pts2 = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
    matrix, _ = cv2.findHomography(pts2, pts1)
    imgOut = cv2.warpPerspective(imgAug, matrix, (img.shape[1], img.shape[0]))
    cv2.fillConvexPoly(img, pts1.astype(int), (0, 0, 0))
    imgOut = img + imgOut
    return imgOut


def main():
    cap = cv2.VideoCapture(2)
    video = cv2.VideoCapture("frame.mov")
    videoAug = cv2.VideoCapture("falcon.mov")
    out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(
        *'MPEG'), 45, (int(video.get(3)), int(video.get(4))))
    while True:
        _, img = cap.read()
        _, imgAug = videoAug.read()
        _, frame = video.read()
        # imgOut = img
        corners, ids = findArucoMarkers(frame)

        if ids is not None:
            if len(ids) > 0:
                print(ids)
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

        cv2.namedWindow("arUco", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Augment", cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Augment', 800, 450)
        cv2.resizeWindow('arUco', 800, 450)
        cv2.imshow("Augment", frame)
        cv2.imshow("arUco", imgOut)
        out.write(imgOut)
        key = cv2.waitKey(1)
        if key == 27 or key == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    main()
