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
parser.add_argument('--scenes', '-s', type=argparse.FileType('r'))
parser.add_argument('--output', '-o', type=argparse.FileType('wb'))

args = parser.parse_args()

logging.basicConfig(format='%(levelname)s %(message)s')
logger = logging.getLogger('keyframe_cluster')
logger.setLevel(10)


class Scene(object):
    def __init__(self, start_frame, end_frame, duration_s):
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.duration_s = duration_s


# grab the list of scenes
scenes = []
# skip over the first line in the scenes file which is garbage
args.scenes.readline()
reader = csv.DictReader(args.scenes)
for scene_dict in reader:
    start_frame = int(scene_dict['Frame Number (Start)'])
    duration = float(scene_dict['Length (seconds)'])
    frame_rate = 20
    end_frame = int(start_frame + duration * frame_rate)
    scene = Scene(start_frame=start_frame, end_frame=end_frame, duration_s=duration)
    scenes.append(scene)

# open the video file
video = imageio.get_reader(args.video, 'ffmpeg')


# grab frame as YCbCr
def grab_frame(number):
    rgb = video.get_data(number)
    img = Image.fromarray(rgb)
    ycbcr = img.convert('YCbCr')
    # frames can be really small for the clustering
    new_width = int(ycbcr.width * (64.0 / ycbcr.height))
    new_width = 80
    ycbcr = ycbcr.resize((new_width, 64))
    return np.asarray(ycbcr, np.uint8)


def blocks(f):
    dim = 4
    assert f.shape[0] % dim == 0
    assert f.shape[1] % dim == 0
    blocks = []
    for i in range(int(f.shape[0]/float(dim))):
        si = i * dim
        ei = si + dim
        for j in range(int(f.shape[1]/float(dim))):
            sj = j * dim
            ej = sj + dim
            block = f[si:ei, sj:ej]
            # convert block into average of YUV
            block = np.mean(block, axis=-1)
            blocks.append(block)
    return np.array(blocks)


def block_matching(f1, f2):
    f1 = blocks(f1)
    f2 = blocks(f2)
    match = []
    for block in f2:
        # find matching block in f1
        differences = np.abs(f1 - block)
        differences = np.sum(differences, axis=(1, 2))
        closest = differences.argmin()
        # closest = sys.maxsize
        # for b2 in f1:
        #     dist = np.sum(np.abs(b2 - block))
        #     if dist < closest:
        #         closest = dist
        match.append(closest / len(f1))
    return match


# frame discontinuity is defined as the average distance between blocks
def discontinuity(f1, f2):
    matchings = block_matching(f1, f2)
    return np.mean(matchings)


def keyframe_in_cluster(cluster):
    # TODO: more sophistated keyframe selection
    # keyframe_index = int(len(cluster) / 2)
    keyframe_index = random.randrange(len(cluster))
    keyframe_number = cluster[keyframe_index]
    keyframe = video.get_data(keyframe_number)
    return keyframe_number, keyframe


keyframes = []

shot_clusters = []
# now cluster the frames in each scene and pick a keyframe
for scene in scenes:
    # grab all the frames in this shot
    frames = [grab_frame(f) for f in range(scene.start_frame, scene.end_frame)]
    logger.info('%d frames in shot', len(frames))
    # a cluster is a list of frames that belong in that cluster
    clusters = []
    # start off with the first frame in its own cluster
    clusters.append([0])
    # for each frame k, if the difference between frame k-1 and frame k is
    # greater than a threshold T, create a new cluster
    T = 0.4
    for frame, (cur, prev) in tqdm(enumerate(zip(frames[1:], frames)), total=len(frames)):
        d = discontinuity(prev, cur)
        if d > T:
            clusters.append([frame])
        else:
            clusters[-1].append(frame)
    logger.info('Shot resulted in %d clusters', len(clusters))

    scene.clusters = clusters
    # pick the largest cluster to choose the keyframe in
    cluster = sorted(clusters, key=lambda c: len(c), reverse=True)[0]
    keyframe_number, keyframe = keyframe_in_cluster(cluster)
    keyframes.append((keyframe_number, scene.start_frame, scene.duration_s, keyframe))


target_keyframes = 24
# if we wanted more keyframes, look at the longest shots to come up with more
while len(keyframes) < target_keyframes:
    logger.info('Getting another keyframe (%d < %d)', len(keyframes), target_keyframes)
    # TODO: take into account how many keyframes we already picked from this shot
    shot = sorted(scenes, key=lambda s: s.duration_s, reverse=True)[0]
    # pick the biggest cluster in that shot
    cluster = sorted(shot.clusters, key=lambda c: len(c), reverse=True)[0]
    keyframe_number, keyframe = keyframe_in_cluster(cluster)
    keyframes.append((keyframe_number, shot.start_frame, shot.duration_s, keyframe))


pickle.dump(keyframes, args.output)
