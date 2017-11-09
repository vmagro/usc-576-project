Input file conversion:  
provided program `convert.go` converts the provided rgb video format and
converts it to rgb24. `ffmpeg` is then able to work with the resulting rgb24
video.

Example:
```
./rgb2mp4 ~/Downloads/Disney.rgb ~/Downloads/Disney.wav ./Disney.mp4
```
This is roughly equivalent to the following commands:  
```
go run convert.go -in=/home/vmagro/Downloads/Disney.rgb  -out=(pwd)/converted.rgb
ffmpeg -framerate 20 -vcodec rawvideo -f rawvideo -pix_fmt rgb24 -s 352x288 -i ./converted.rgb -i raw.wav -pix_fmt yuv420p converted.mp4
```
This converts the course provided Disney video to rgb24 format, then converts
that rgb24 video into an mp4 with synced audio from the given wav file.
