#!/bin/bash
set -e

video="output.mp4"

# use scenedetect to detect the scenes
scenes="$video".scenes.csv
scenedetect -i "$video" --csv-output "$scenes"

# use the keyframe clustering program to pick out a keyframe from each scene
keyframes="$video".keyframes.pkl
./keyframe_cluster.py -v "$video" -s "$scenes" -o "$keyframes"

# now generate a tapestry from those keyframes
./gen_tapestry.py -k "$keyframes"

# now everything will be processed and opening ui/index.html will show the video and the tapestry
