import numpy as np
import cv2
import cv2 as cv
import glob


# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*9,3), np.float32) # thay doi do dai
objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2) # thay doi
objp = objp*3
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
images = glob.glob('anhq/*.jpg')
# anh = 0
for fname in images:
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (9,6), None)# thay doi
    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)
        # Draw and display the corners
        cv.drawChessboardCorners(img, (9,6), corners2, ret) # thay doi
        cv.imshow('img', img)
        # name = 'picture' + str(anh) + '.jpg'
        # cv2.imwrite(name, img)
        # anh += 1
        cv.waitKey(500)
cv.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

print("Camera matrix : \n")
print(mtx)
print("dist : \n")
print(dist)
print('\n')
print("rvecs : \n")
print(rvecs)
print('\n')
print("tvecs : \n")
print(tvecs)
print('\n')


# A = {
#   "mtx": mtx,
#   "dist": dist,
# }
# with open('SAVE.pickle', 'wb') as handle:
#     pickle.dump(A, handle, protocol=pickle.HIGHEST_PROTOCOL)
# del A
# with open('SAVE.pickle', 'rb') as handle:
#     B = pickle.load(handle)
# print(B["mtx"])
# print(B["dist"])

np.savez('laptop.npz', mtx=mtx, dist=dist)
# with np.load('nghiep.npz') as X:
#     camera_matrix, dist_coeff = [X[i] for i in ('mtx', 'dist')]
#     print(camera_matrix)
#     print(dist_coeff)