"""
SVG Image Extractor

Usage:
  svgex.py <input-svg> <image-directory> [-r] [--out=<path>]

Options:
  -h --help     Show this screen.
  --out=<path>  Output path [default:]
  -r            Remove duplicate images.
"""

import mimetypes
import base64
from collections import namedtuple
import os
import itertools
from hashlib import sha1

import docopt
from lxml.etree import XMLParser, parse

ImageData = namedtuple('ImageData', 'data extension id')

IMAGE_QN = '{http://www.w3.org/2000/svg}image'
HREF_QN = '{http://www.w3.org/1999/xlink}href'

ABSREF_QN = '{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}absref'

FINDALL_FORMAT = './/{}'


def iter_all_images(tree):
    return tree.iterfind(FINDALL_FORMAT.format(IMAGE_QN))


class NoEmbeddedImage(Exception):
    pass


def get_extension(url):
    return mimetypes.guess_extension(mimetypes.guess_type(url)[0])


def get_image_data(image):
    href = image.attrib[HREF_QN]
    if not href.startswith('data:'):
        raise NoEmbeddedImage('No image is embedded in this element.')

    extension = get_extension(href)
    data = base64.decodestring(href.split(',', 1)[1])
    id_ = image.attrib['id']

    return ImageData(data, extension, id_)


def save_image(target_directory, image_data):
    data, extension, id_ = image_data

    target_path = None  # Only to assist editors and linters. It is not really needed here.

    for index in itertools.count():
        target_path = os.path.join(target_directory,
                                   '{}{}{}'.format(os.path.basename(id_),
                                                   index if index else '',
                                                   extension))
        if os.path.exists(target_path):
            continue

        with open(target_path, 'wb') as f:
            f.write(data)
            break

    return target_path


def set_image_data(image, image_path):
    image.attrib[HREF_QN] = image_path


def get_image_hash(image_data):
    return sha1(image_data.data).digest()


def parse_svg(svg_path):
    p = XMLParser(huge_tree=True)
    return parse(svg_path, parser=p)

def extract_all_images(svg_path, target_directory, new_svg_path=None, remove_dups=False):
    tree = parse_svg(svg_path)
    svg_dir = os.path.dirname(svg_path)

    if new_svg_path:
        new_svg_path = os.path.join(svg_dir, new_svg_path)
    else:
        new_svg_path = ''

    new_svg_dir = os.path.dirname(new_svg_path)

    image_log = {}

    for image in iter_all_images(tree):
        try:
            image_data = get_image_data(image)

            # noinspection PyTypeChecker
            image_hash = get_image_hash(image_data)

            if remove_dups and image_hash in image_log:
                image_path = image_log[image_hash]
            else:
                target_path = os.path.join(svg_dir, target_directory)
                image_path = save_image(target_path, image_data)

                if not os.path.isabs(target_directory):
                    image_path = os.path.relpath(image_path, new_svg_dir)

            set_image_data(image, image_path)
            image_log[image_hash] = image_path

        except NoEmbeddedImage:
            pass

    if new_svg_path:
        tree.write(new_svg_path, pretty_print=True)


def main():
    arguments = docopt.docopt(__doc__)

    svg_path = arguments['<input-svg>']
    image_directory = arguments['<image-directory>']
    new_svg_path = arguments['--out']
    remove_dups = arguments['-r']

    print ("  ____________   ____________       ____  ___\n"
           " /   _____\   \ /   /  _____/  ____ \   \/  /\n"
           " \_____  \ \   Y   /   \  ____/ __ \ \     / \n"
           " /        \ \     /\    \_\  \  ___/ /     \ \n"
           "/_______  /  \___/  \______  /\___  /___/\  \ \n"
           "        \/                 \/     \/      \_/")

    print
    print "          The SVG Image Extractor"
    print
    print
    print "Extracting images from '{}' into '{}'.".format(svg_path, image_directory)

    if new_svg_path is 'None':
        print "Creating a new svg file at '{}'.".format(new_svg_path)

    extract_all_images(svg_path, image_directory, new_svg_path, remove_dups)


if __name__ == '__main__':
    main()
