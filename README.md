SVGeX
=====

Get the embedded images out of your oversized SVGs and link them instead!


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

Just run `pip install -r requirements.txt`.