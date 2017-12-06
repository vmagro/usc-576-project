#!/usr/bin/env python3

import argparse
import logging
import csv
from collections import namedtuple
import imageio
import numpy as np
from PIL import Image
from tqdm import tqdm
import pickle
import random

parser = argparse.ArgumentParser()

parser.add_argument('--video', '-v', type=argparse.FileType('rb'))
parser.add_argument('--output', '-o', type=argparse.FileType('wb'))

args = parser.parse_args()

logging.basicConfig(format='%(levelname)s %(message)s')
logger = logging.getLogger('keyframe_every_n')
logger.setLevel(10)


# open the video file
video = imageio.get_reader(args.video, 'ffmpeg')

def grab_frame(number):
    rgb = video.get_data(number)
    return rgb

keyframes = []

num_frames = video.get_length()
target_keyframes = 24
step = int(num_frames / target_keyframes)
duration_s = step / 20.0

for keyframe_number in tqdm(range(0, num_frames, step)):
    keyframe = grab_frame(keyframe_number)
    keyframes.append((keyframe_number, keyframe_number, duration_s, keyframe))

if len(keyframes) > 24:
    keyframes = keyframes[:24]

import pdb; pdb.set_trace()

# sort keyframes by their start time
keyframes = sorted(keyframes, key=lambda k: k[0])

pickle.dump(keyframes, args.output)
