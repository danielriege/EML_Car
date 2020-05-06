#!/usr/bin/env python3
import glob
import sys
import cv2

test_run_name = "test"
if len(sys.argv) > 1:
    test_run_name = sys.argv[1]

img_array = []
size = (0,0)
for filename in sorted(glob.glob("./training_data/*.jpg")):
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width, height)
    img_array.append(img)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter("./training_videos/%s.mp4" % (test_run_name),
                        fourcc, 30, size)
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()
