#!/usr/bin/env python3

import argparse
import numpy as np
import PIL
from PIL import Image
import pickle

frame_rate = 20.0


parser = argparse.ArgumentParser()

parser.add_argument('--keyframes', '-k', type=argparse.FileType('rb'))

args = parser.parse_args()


def timestamp(frame):
    return frame / frame_rate


keyframes = pickle.load(args.keyframes)

keyframes_with_timestamps = [(frame, timestamp(start), timestamp(start) + duration) for i, start, duration, frame in keyframes]
keyframes = [frame for i, start, duration, frame in keyframes]
num_keyframes = len(keyframes_with_timestamps)

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
