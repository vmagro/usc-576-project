#!/usr/bin/env python3

import numpy as np
import PIL
from PIL import Image
import pdb

frame_rate = 20.0


def timestamp(frame):
    return frame / frame_rate


in_file = 'output.rgb'
video = np.fromfile(in_file, dtype=np.uint8)

video = video.reshape((-1, 288, 352, 3))
num_frames = video.shape[0]

num_keyframes = 24
step = int(num_frames / float(num_keyframes))
keyframes = video[0::step][:num_keyframes]
keyframes_with_timestamps = [(k, timestamp(i * step), timestamp(
    (i + 1) * step)) for i, k in enumerate(keyframes)]

tapestry = np.zeros((288 * 2, int(num_keyframes / 2) * 352 + int(352 / 2), 3), np.uint8)

# copy keyframes into tapestry
high = True
for i, keyframe in enumerate(keyframes):
    left = int((i / 2.0)) * 352
    if high:
        tapestry[:288, left:left + 352, :] = keyframe
    else:
        left += int(352 / 2)
        tapestry[288:, left:left + 352, :] = keyframe
    high = not high

img = Image.fromarray(tapestry)
img = img.resize([1408,184], PIL.Image.ANTIALIAS)
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
        left += int(352 / 2)
        top = 288
    high = not high

    left /= 3.125
    top /= 3.125
    width = 352 / 3.125
    height = 288 / 3.125

    line = '{{start: {}, end: {}, left: {}, right: {}, top: {}, bottom: {}}},\n'.format(
        start, end, left, left + width, top, top + height)
    js_out.write(line)

js_out.write('];')
