import cv2
import cv2 as cv
import numpy as np
import cv2.aruco as aruco
import time
import serial  # Khai báo thưu viện serial
# port = "/dev/ttyACM0"
# ser = serial.Serial(port,9600)



# ser = serial.Serial('/dev/ttyACM0',9600)  # Lưu ý x là số cổng USB hồi nãy bạn xem
cap = cv2.VideoCapture(0)

with np.load('laptop.npz') as X:
    mtx, dist = [X[i] for i in ('mtx', 'dist')]
    print(mtx)
    print(dist)

markerLength = 7.1

while (True):
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    dictionary = cv.aruco.Dictionary_get(cv.aruco.DICT_ARUCO_ORIGINAL)
    parameters = cv.aruco.DetectorParameters_create()

    corners, ids, rejectedCandidates = cv.aruco.detectMarkers(frame, dictionary, parameters=parameters)

    font = cv2.FONT_HERSHEY_SIMPLEX
    
    if np.all(ids != None):

        rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, markerLength, mtx, dist)
        a = tvec[0,0,2]
#         if a <= 30:
#            b= str(a)
#            ser.write(b.encode())
#            time.sleep(1)
#            print(b)
        for i in range(0, ids.size):
            # draw axis for the aruco markers
            aruco.drawAxis(frame, mtx, dist, rvec[i], tvec[i], 3)
        # draw a square around the markers
        aruco.drawDetectedMarkers(frame, corners, ids, (255,0,0))

        # code to show ids of the marker found
        strg = ''
        for i in range(0, ids.size):

            strg += str(tvec[i][0]) + ','
            cv2.putText(frame,"TVEC: " + strg , (0, 64), font, 0.7, (0, 255, 0), 2, cv2.LINE_AA)

    else:
        # code to show 'No Ids' when no markers are found
        cv2.putText(frame, "No Ids", (0, 64), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()