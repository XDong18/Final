import numpy as np
from computeP import computeP
import json 
import cv2
import skvideo.io as vio
import skimage.io as io


def draw(img, imgpts):
    imgpts = np.int32(imgpts).reshape(-1,2)
    # draw ground floor in green
    img = cv2.drawContours(img, [imgpts[:4]],-1,(0,255,0),-3)
    # draw pillars in blue color
    for i,j in zip(range(4),range(4,8)):
        img = cv2.line(img, tuple(imgpts[i]), tuple(imgpts[j]),(255),3)
    # draw top layer in red color
    img = cv2.drawContours(img, [imgpts[4:]],-1,(0,0,255),3)
    return img

def main():
    with open('./pts/all_pts3.json') as f:
        all_pts2d = json.load(f)
        print(len(all_pts2d))
    with open('./pts/pts3d.json') as f:
        pts3d = json.load(f)

    axis = np.float32([[0,0,0], [0,5,0], [5,5,0], [5,0,0],
                [0,0,5],[0,5,5],[5,5,5],[5,0,5] ])              
    axis = np.concatenate([axis, np.ones((8,1), dtype=np.float32)], axis=1)

    video = vio.vread('./video/video3.MOV')
    new_video = video[:]
    print(len(video))
    for i, frame in enumerate(video):
        if i>len(all_pts2d)-1:
            break
        bgr_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        pts2d = all_pts2d[i]
        P = computeP(np.array(pts3d), np.array(pts2d))
        axis2d = np.dot(P, axis.T)
        axis2d[0] = axis2d[0] / axis2d[2]
        axis2d[1] = axis2d[1] / axis2d[2]
        axis2d = axis2d[:2].T
        new_img = draw(bgr_frame, axis2d)
        rgb_img = cv2.cvtColor(new_img, cv2.COLOR_BGR2RGB)
        new_video[i] = rgb_img

    vio.vwrite('./test.avi', new_video)

if __name__ == "__main__":
    main()



    