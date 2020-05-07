import json 


h = 7.1 / 2
w = 24.2 / 5 
l = 14.3 / 3
pts3d = [[0, 2*l, 0], [w, 2*l, 0], [2*w, 2*l, 0], [3*w, 2*l, 0],
        [0, l, 0], [w, l, 0], [2*w, l, 0], [3*w, l, 0],
        [0, 0, 0], [w, 0, 0], [2*w, 0, 0], [3*w, 0, 0],
        [0, 0, -h], [w, 0, -h], [2*w, 0, -h], [3*w, 0, -h]]

print(pts3d)
with open('./pts/pts3d.json', 'w') as f:
    json.dump(pts3d, f)