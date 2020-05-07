import trimesh
import pyrender
import numpy as np
import cv2
import matplotlib.pyplot as plt
import json
from computeP import computeP
from scipy.spatial.transform import Rotation as R


r = R.from_euler('xyz', [0,0,0], degrees=True)
print(r.as_matrix())
with open('./pts/all_pts3.json') as f:
    all_pts2d = json.load(f)
with open('./pts/pts3d.json') as f:
    pts3d = json.load(f)

img = cv2.imread('./frame0.png')
P = computeP(np.array(pts3d), np.array(all_pts2d[0]))
# P = P * (1./P[2,3])

cameraMatrix, rotMatrix, transVect, rotMatrixX, rotMatrixY, rotMatrixZ, eulerAngles = cv2.decomposeProjectionMatrix(P)
# ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(np.array([pts3d], dtype=np.float32), np.array([all_pts2d[0][:12]], dtype=np.float32), img.shape[1::-1], None, None)
# rotation = cv2.Rodrigues(rvecs)
# position = np.eye(4)
# position[:3,:3] = rotation
# position[:, 3] = tvecs
fy = cameraMatrix[1,1] / cameraMatrix[2,2]

print(rotMatrix)
print(cameraMatrix / cameraMatrix[2,2])
print(transVect / transVect[3])
print(eulerAngles)
