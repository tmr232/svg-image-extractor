SVGeX
=====

Extract all images from your oversized SVGs and turn them from embedded images to linked images.


Usage
-----
```
Usage:
  svgex.py <input-svg> <image-directory> [--output-svg=<path>]
Options:
  -h --help            Show this screen.
  --output-svg=<path>  Output path [default:]
```

The `image-directory` can be an absolute or a relative path. This will be reflected in the resulting SVG file as well.

All relative paths are relative to the `input-svg` path.

The script does not create directories at this point.


Dependencies
------------

- lxml
- docopt
