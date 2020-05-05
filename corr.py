import skvideo.io as vio
import numpy as np 
import os
from matplotlib.pyplot import ginput
import json
import matplotlib.pyplot as plt

fn = "./video.MOV"
frames = vio.vread(fn)
first_frame = frames[0]
plt.imshow(first_frame)
pts_list = ginput(n=-1, timeout=0)
with open('./pts.json', 'w') as f:
    json.dump(pts_list, f)

