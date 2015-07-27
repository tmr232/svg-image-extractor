SVGeX
=====

Extract all images from your oversized SVGs and turn them from embedded images to linked images.


Usage
-----
```
Usage:
  svgex.py <input-svg> <image-directory> [-r] [--out=<path>]

Options:
  -h --help     Show this screen.
  --out=<path>  Output path [default:]
  -r  
```

The `image-directory` can be an absolute or a relative path. This will be reflected in the resulting SVG file as well.

All relative paths are relative to the `input-svg` path.

The script does not create directories at this point.

Use `-r` if you want to remove duplicate images.

Use `--out=some_path` to create an SVG with all the images linked to it, instead of embedded.


Dependencies
------------

- lxml
- docopt
