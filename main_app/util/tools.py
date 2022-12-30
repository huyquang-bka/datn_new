import cv2
import numpy as np


polygon = [[526, 166], [25, 596], [1911, 595], [1912, 451], [1496, 144]]
polygon = np.array(polygon, np.int32)
polygon = polygon.reshape((-1, 1, 2))

def is_in_polygon(centroid, polygon):
    return cv2.pointPolygonTest(polygon, centroid, False) >= 0

def count_object(old_dict, new_dict, polygon):
    mapping = {2: "car", 3: "motorbike", 5: "bus", 7: "motorbike"}
    count_dict = {"car": 0, "truck": 0, "bus": 0, "motorbike": 0}
    for key, value in new_dict.items():
        if not key in old_dict:
            continue
        x1, y1, x2, y2, cls = value
        x1_old, y1_old, x2_old, y2_old, cls_old = old_dict[key]
        centroid_new = ((x1 + x2) / 2, (y1 + y2) / 2)
        centroid_old = ((x1_old + x2_old) / 2, (y1_old + y2_old) / 2)
        if is_in_polygon(centroid_old, polygon) and not is_in_polygon(centroid_new, polygon):
            count_dict[mapping[cls]] += 1
    return count_dict

        
if __name__ == "__main__":
    old_dict = {1: [800, 400, 802, 402, 2], 2: [1, 1, 2, 2, 3], 3: [1, 1, 2, 2, 5], 4: [1, 1, 2, 2, 7]}
    new_dict = {1: [1, 1, 2, 2, 2], 2: [1, 1, 2, 2, 3], 3: [1, 1, 2, 2, 5], 4: [1, 1, 2, 2, 7], 5: [1, 1, 2, 2, 2]}
    print(count_object(old_dict, new_dict, polygon))
        