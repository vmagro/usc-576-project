#!/usr/bin/env python3

import numpy as np
from PIL import Image
import pdb

frame_rate = 20.0


def timestamp(frame):
    return frame / frame_rate


in_file = 'converted.rgb'
video = np.fromfile(in_file, dtype=np.uint8)

video = video.reshape((-1, 288, 352, 3))
num_frames = video.shape[0]

step = int(num_frames / 16.0)
keyframes = video[0::step][0:16]
keyframes_with_timestamps = [(k, timestamp(i * step), timestamp(
    (i + 1) * step)) for i, k in enumerate(keyframes)]

tapestry = np.zeros((288 * 2, int(len(keyframes) / 2) * 352, 3), np.uint8)

# copy keyframes into tapestry
high = True
for i, keyframe in enumerate(keyframes):
    left = int((i / 2.0)) * 352
    if high:
        tapestry[:288, left:left + 352, :] = keyframe
    else:
        tapestry[288:, left:left + 352, :] = keyframe
    high = not high

img = Image.fromarray(tapestry)
img.save('tapestry.png')

js_out = open('tapestry.js', 'w')
js_out.write('var tapestry_regions = [\n')
high = True
for i, (_, start, end) in enumerate(keyframes_with_timestamps):
    left = int((i / 2.0)) * 352
    top = 0
    if high:
        top = 0
    else:
        top = 288
    high = not high

    line = '{{start: {}, end: {}, left: {}, right: {}, top: {}, bottom: {}}},\n'.format(
        start, end, left, left + 352, top, top + 288)
    js_out.write(line)

js_out.write('];')
