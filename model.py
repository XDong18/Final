import trimesh
import pyrender
import numpy as np
import cv2
import matplotlib.pyplot as plt
import json
from computeP import computeP



with open('./pts/all_pts3.json') as f:
    all_pts2d = json.load(f)
with open('./pts/pts3d.json') as f:
    pts3d = json.load(f)[:12]

img = cv2.imread('./frame0.png')
# P = computeP(np.array(pts3d), np.array(all_pts2d[0]))

# cameraMatrix, rotMatrix, transVect, rotMatrixX, rotMatrixY, rotMatrixZ, eulerAngles = cv2.decomposeProjectionMatrix(P)
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(np.array([pts3d], dtype=np.float32), np.array([all_pts2d[0][:12]], dtype=np.float32), img.shape[1::-1], None, None)
print(ret, mtx)
print(dist)
print(rvecs)
print(tvecs)
