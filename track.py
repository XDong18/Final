import cv2
import sys
import json
import numpy as np

class p_track(object):
    def __init__(self, location, idx):
        self.ini_location = location.astype(np.int32)
        self.idx = idx
        self.bbox = None
    
    def tracker_init(self, frame):
        self.tracker = cv2.TrackerGOTURN_create()
        bbox = (self.ini_location[0] - 8, self.ini_location[1] - 8, \
                self.ini_location[0] + 8, self.ini_location[1] + 8)
        # print(bbox)

        self.bbox = bbox
        self.tracker.init(frame, bbox)
    
    def bbox_update(self, frame):
        ok, bbox = self.tracker.update(frame)
        self.bbox = bbox
        return ok, [(bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2]

def main():
    with open('./pts.json') as f:
        pts_list = json.load(f)

    all_pts_list = []
    all_pts_list.append(pts_list)

    p_track_list = []
    for i, pts in enumerate(pts_list):
        p_track_list.append(p_track(np.array(pts), i))

    video = cv2.VideoCapture("video.MOV")
    if not video.isOpened():
        print("Could not open video")
        sys.exit()

    # Read first frame.
    ok, frame = video.read()
    if not ok:
        print('Cannot read video file')
        sys.exit()
    
    for p in p_track_list:
        p.tracker_init(frame)
    
    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break

        # Update tracker
        temp_pts_list = []
        for p in p_track_list:
            ok, new_pts = p.bbox_update(frame)
            temp_pts_list.append(new_pts)
            bbox = p.bbox
            if ok:
            # Tracking success
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[2]), int(bbox[3]))
                cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
            else :
            # Tracking failure
                cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
        
        all_pts_list.append(temp_pts_list)
        # Display result
        cv2.imshow("Tracking", frame)

        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27 : break
    
    with open('./all_pts.json', 'w') as f:
        json.dump(all_pts_list, f)

if __name__ == "__main__":
    main()