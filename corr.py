import skvideo.io as vio
import numpy as np 
import os
from matplotlib.pyplot import ginput
import json
import matplotlib.pyplot as plt

fn = "./video/video2.MOV"
frames = vio.vread(fn)
print(len(frames))
first_frame = frames[0]
plt.imshow(first_frame)
pts_list = ginput(n=-1, timeout=0)
with open('./pts/pts2.json', 'w') as f:
    json.dump(pts_list, f)

