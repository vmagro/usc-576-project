#!/bin/sh
set -e

video=$1
audio=$2
output=$3

converted_rgb=$(mktemp)
go run convert.go -in=$1 -out=$converted_rgb

ffmpeg -y -framerate 20 -vcodec rawvideo -f rawvideo -pix_fmt rgb24 -s 352x288 -i $converted_rgb -i $audio -pix_fmt yuv420p $3
