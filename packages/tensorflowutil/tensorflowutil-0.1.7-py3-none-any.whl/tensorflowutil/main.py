import os
import sys
import argparse
import tensorflow as tf

RELPATH = os.path.dirname(os.path.realpath(__file__))
# __vesion__ = x.x.x
with open(os.path.join(RELPATH, "version.py")) as f:
    exec(f.read())

PACKAGENAME = os.path.split(RELPATH)[1]


def display_version():
    print("Package: {} \nVersion: {}".format(PACKAGENAME, __version__))


def arguments_parser(argv):
    parser = argparse.ArgumentParser(
        description='Process arguments for {}'.format(PACKAGENAME))
    parser.add_argument('--version',
                        '-v',
                        action='store_true',
                        help='Version of {}'.format(PACKAGENAME))
    args = parser.parse_args(argv)
    return args


def main():
    # print("Entrypoint: {}, tensorflow version: {}".format(
    #    __name__, tf.__version__))
    args = arguments_parser(sys.argv[1:])

    if args.version:
        display_version()
    else:
        pass


if __name__ == '__main__':
    main()
