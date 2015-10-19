#!/usr/bin/env python3
import argparse
import json
import os
import shutil
import sys


DESCRIPTION = """\
Generates a searchable table of content for the Android SDK documentation.
"""


BLACKLISTED_DIRS = ('internal', 'test')


def walk_doc(doc_dir):
    for root, dirs, filenames in os.walk(doc_dir):
        for blacklisted_dir in BLACKLISTED_DIRS:
            try:
                dirs.remove(blacklisted_dir)
            except ValueError:
                pass
        for filename in filenames:
            if filename[0].isupper():
                class_name = os.path.splitext(filename)[0]
                file_path = os.path.join(root, filename)
                yield dict(name=class_name, path=file_path)


def main():
    parser = argparse.ArgumentParser()
    parser.description = DESCRIPTION

    parser.add_argument('-o', '--output', dest='output_dir', default='.',
                        help='write toc to DIR', metavar='DIR')

    parser.add_argument('reference_dir')

    args = parser.parse_args()

    ASSETS_DIR = os.path.dirname(__file__)
    shutil.copy(os.path.join(ASSETS_DIR, 'toc.html'), args.output_dir)
    shutil.copy(os.path.join(ASSETS_DIR, 'list.min.js'), args.output_dir)

    lst = list(walk_doc(args.reference_dir))
    lst.sort(key=lambda x: x['name'])

    with open(os.path.join(args.output_dir, 'values.js'), 'wt') as f:
        f.write('values = ')
        json.dump(lst, f, indent=4)
        f.write(';')

    return 0


if __name__ == '__main__':
    sys.exit(main())
# vi: ts=4 sw=4 et
