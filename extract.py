#!/usr/bin/env python3

import pickle
from PIL import Image


keyframes = pickle.load(open('output.mp4.keyframes.pkl', 'rb'))

for i, start, duration, frame in keyframes:
    Image.fromarray(frame).save('tmp/{}.png'.format(i))
