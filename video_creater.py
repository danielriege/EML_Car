#!/usr/bin/env python3
import glob
import sys
import cv2

test_run_name = "test"
if len(sys.argv) > 0:
    test_run_name = sys.argv[0]

img_array = []
size = (0,0)
for filename in sorted(glob.glob("./training_data/*.jpg")):
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width, height)
    img_array.append(img)
out = cv2.VideoWriter("./training_videos/%s.avi" % (test_run_name),
                        cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()


