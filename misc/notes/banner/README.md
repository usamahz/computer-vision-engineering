# Banner

`misc/banner-calibration-chessboard.avif` is a camera calibration frame rendered as its own pixel values. Each cell of the grid is one sample of the image, and the glyph printed in that cell is the sample's 8-bit luminance in hex. White squares read `ff`, black squares read near `00`, and the edges between them carry the in-between values a corner detector works from. Read closely, the banner is the array a calibration routine sees. Step back and it is the chessboard again.

Calibration is where much of computer vision engineering starts: before a pixel can be trusted as a measurement, the camera that took it has to be modelled.

## Source

`left01.jpg` from the OpenCV sample data (`samples/data` in the opencv/opencv repository, Apache 2.0). It is the first frame of the stereo calibration sequence used in the OpenCV calibration tutorial.

## Command

```sh
python3 misc/notes/banner/render.py --src left01.jpg --out misc/banner-calibration-chessboard.avif \
  --crop 0,0.09,1,0.578 --cell 16 --contrast 1.05 --detail 1.0 --base 0.42 \
  --gain 1.05 --lift 34 --sat 1.0 --colour 1.0
```

Output is 3000x1100 at AVIF quality 64. `--mode bayer` prints the RGGB mosaic value of each cell instead of luminance.

The file is named after its source because GitHub caches images by path. Render a new banner under a new name instead of overwriting this one.
