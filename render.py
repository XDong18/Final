import trimesh
import pyrender
import numpy as np
import cv2
import matplotlib.pyplot as plt
import json
from computeP import computeP
from scipy.spatial.transform import Rotation as R
import sys


def single():
    with open('./pts/all_pts3.json') as f:
        all_pts2d = json.load(f)
    with open('./pts/pts3d.json') as f:
        pts3d = json.load(f)

    P = computeP(np.array(pts3d), np.array(all_pts2d[0]))
    cameraMatrix, rotMatrix, transVect, rotMatrixX, rotMatrixY, rotMatrixZ, eulerAngles = cv2.decomposeProjectionMatrix(P)
    img = cv2.imread('./frame0.png')
    fy = cameraMatrix[1,1] / cameraMatrix[2,2]
    fov = 2 * np.arctan(img.shape[1] / (2 * fy))
    print(fov)
    position = np.eye(4)
    position[:3,:3] = rotMatrix
    position[:3, 3] = (transVect[:3] / transVect[3]).reshape(-1) 
    print(position)


    fuze_trimesh = trimesh.load('examples/models/fuze.obj')
    fuze_trimesh.vertices = fuze_trimesh.vertices * 500
    mesh = pyrender.Mesh.from_trimesh(fuze_trimesh)

    r = R.from_euler('xyz', [0,0,-0], degrees=True)

    drill_pose = np.eye(4)
    drill_pose[:3, :3] = r.as_matrix()
    drill_pose[0,3] = 0
    drill_pose[1,3] = 50
    drill_pose[2,3] = -np.min(fuze_trimesh.vertices[:,2]) + 30
    scene = pyrender.Scene(bg_color=np.array([0, 0, 0, 0]))
    scene.add(mesh, pose=drill_pose)
    camera = pyrender.PerspectiveCamera(yfov=np.pi/1.1, aspectRatio=img.shape[1]/img.shape[0])

    # camera_pose = np.array([
    #     [1.0,  0.,   0.,   1.],
    #     [0.0,  1.0, 0.0, 1.0],
    #     [0.0,  0.,   1.,   1.],
    #     [0.0,  0.0, 0.0, 1.0],
    # ])
    scene.add(camera, pose=position)
    light = pyrender.SpotLight(color=np.ones(3), intensity=100000,
                                innerConeAngle=np.pi/3,
                                outerConeAngle=np.pi/2)
    scene.add(light, pose=position)
    r = pyrender.OffscreenRenderer(img.shape[1], img.shape[0])
    color, depth = r.render(scene)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
    img_rgb[gray!=0] = color[gray!=0]

    plt.figure()
    plt.imshow(img_rgb)
    plt.show()

def main():
    with open('./pts/all_pts3.json') as f:
        all_pts2d = json.load(f)
    with open('./pts/pts3d.json') as f:
        pts3d = json.load(f)

    fuze_trimesh = trimesh.load('examples/models/fuze.obj')
    fuze_trimesh.vertices = fuze_trimesh.vertices * 500
    img = cv2.imread('./frame0.png')
    mesh = pyrender.Mesh.from_trimesh(fuze_trimesh)
    camera = pyrender.PerspectiveCamera(yfov=np.pi/1.1, aspectRatio=img.shape[1]/img.shape[0])
    light = pyrender.SpotLight(color=np.ones(3), intensity=100000,
                            innerConeAngle=np.pi/3,
                            outerConeAngle=np.pi/2)
    r = R.from_euler('xyz', [0,0,-0], degrees=True)
    drill_pose = np.eye(4)
    drill_pose[:3, :3] = r.as_matrix()
    drill_pose[0,3] = 0
    drill_pose[1,3] = 50
    drill_pose[2,3] = -np.min(fuze_trimesh.vertices[:,2]) + 30
    video = cv2.VideoCapture("./video/video3.MOV")
    if not video.isOpened():
        print("Could not open video")
        sys.exit()

    # Read first frame.
    ok, frame = video.read()
    if not ok:
        print('Cannot read video file')
        sys.exit()
    idx = 0
    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break
        if idx > len(all_pts2d) - 1 :
            break
        
        fuze_trimesh = trimesh.load('examples/models/fuze.obj')
        fuze_trimesh.vertices = fuze_trimesh.vertices * 500
        mesh = pyrender.Mesh.from_trimesh(fuze_trimesh)
        camera = pyrender.PerspectiveCamera(yfov=np.pi/1.1, aspectRatio=img.shape[1]/img.shape[0])
        light = pyrender.SpotLight(color=np.ones(3), intensity=100000,
                                innerConeAngle=np.pi/3,
                                outerConeAngle=np.pi/2)
        r = R.from_euler('xyz', [0,0,-0], degrees=True)
        drill_pose = np.eye(4)
        drill_pose[:3, :3] = r.as_matrix()
        drill_pose[0,3] = 0
        drill_pose[1,3] = 50
        drill_pose[2,3] = -np.min(fuze_trimesh.vertices[:,2]) + 30
        P = computeP(np.array(pts3d), np.array(all_pts2d[idx]))
        _, rotMatrix, transVect, _, _, _, _ = cv2.decomposeProjectionMatrix(P)
        position = np.eye(4)
        position[:3,:3] = rotMatrix
        position[:3, 3] = (transVect[:3] / transVect[3]).reshape(-1) 
        print(position)
        scene = pyrender.Scene(bg_color=np.array([0, 0, 0, 0]))
        scene.add(mesh, pose=drill_pose)
        scene.add(camera, pose=position)
        scene.add(light, pose=position)

        r = pyrender.OffscreenRenderer(frame.shape[1], frame.shape[0])
        color, depth = r.render(scene)

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
        img_rgb[gray!=0] = color[gray!=0]
        img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
        # plt.figure()    
        # plt.imshow(color)
        # plt.show()
        # Display result
        cv2.imshow("Tracking", img_bgr)

        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27 : break
        idx += 1

if __name__ == "__main__":
    main()
