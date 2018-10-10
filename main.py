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


def find_doc_items(doc_dir):
    """
    Generate a list of dicts with keys `name` and `path`
    """
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


def copy_static_files(assets_dir, output_dir):
    shutil.copy(os.path.join(assets_dir, 'toc.html'), output_dir)
    shutil.copy(os.path.join(assets_dir, 'list.min.js'), output_dir)


def generate_values_js(fp, doc_items):
    """
    Generate the .js file used by list.min.js
    """
    lst = list(doc_items)
    lst.sort(key=lambda x: x['name'])

    fp.write('values = ')
    json.dump(lst, fp, indent=4)
    fp.write(';')


def main():
    parser = argparse.ArgumentParser()
    parser.description = DESCRIPTION

    parser.add_argument('-o', '--output', dest='output_dir', default='.',
                        help='write toc to DIR', metavar='DIR')

    parser.add_argument('reference_dir')

    args = parser.parse_args()

    doc_items = find_doc_items(args.reference_dir)
    copy_static_files(os.path.dirname(__file__), args.output_dir)
    with open(os.path.join(args.output_dir, 'values.js'), 'wt') as fp:
        generate_values_js(fp, doc_items)

    return 0


if __name__ == '__main__':
    sys.exit(main())
# vi: ts=4 sw=4 et
