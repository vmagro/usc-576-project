package main

/**
 * This program takes the class-provided RGB video and converts it to a sane
 * rgb24 format that can then be processed by ffmpeg.  We read in the R, G and
 * B value for each pixel in each frame and combine them into one frame that
 * has 24 bits per pixel rather than the given 1 color channel per frame.
 */

import (
	"flag"
	"fmt"
	"os"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func main() {
	in := flag.String("in", "", "input rgb video")
	out := flag.String("out", "", "output rgb video")
	flag.Parse()

	fmt.Println(*in)
	fmt.Println(*out)

	inFile, err := os.Open(*in)
	defer inFile.Close()
	check(err)
	outFile, err := os.OpenFile(*out, os.O_RDWR|os.O_CREATE, 0755)
	defer outFile.Close()
	check(err)

	// TODO make changeable
	width := 352
	height := 288

	stat, err := inFile.Stat()
	check(err)
	numFrames := stat.Size() / int64(width*height*3)

	fmt.Printf("Converting %d frames\n", numFrames)

	red := make([]byte, width*height)
	green := make([]byte, width*height)
	blue := make([]byte, width*height)
	combined := make([]byte, width*height*3)
	for frame := int64(0); frame < numFrames; frame++ {
		// TODO: error checking
		read, e := inFile.Read(red)
		if read != width*height {
			panic(fmt.Errorf("Only read %d bytes", read))
		}
		check(e)
		read, e = inFile.Read(green)
		if read != width*height {
			panic(fmt.Errorf("Only read %d bytes", read))
		}
		check(e)
		read, e = inFile.Read(blue)
		if read != width*height {
			panic(fmt.Errorf("Only read %d bytes", read))
		}
		check(e)

		// interleave them into one frame
		// each pixel is 3 bytes, one R one G one B
		for i := 0; i < height; i++ {
			for j := 0; j < width; j++ {
				idx := i*width + j
				combined[idx*3] = red[idx]
				combined[idx*3+1] = green[idx]
				combined[idx*3+2] = blue[idx]
			}
		}
		outFile.Write(combined)
	}
}
