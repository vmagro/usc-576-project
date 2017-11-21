Input file conversion:  
provided program `convert.go` converts the provided rgb video format and
converts it to rgb24. `ffmpeg` is then able to work with the resulting rgb24
video.

Example:
```
./rgb2mp4 ~/Downloads/Disney.rgb ~/Downloads/Disney.wav ./Disney

# This will produce two files, ./Disney.mp4 and ./Disney.mp3
```
This converts the course provided Disney video to rgb24 format, then converts
that rgb24 video into an mp4 and converts the provided wav audio to mp3.
