#!/bin/python3
"""
    YTCP - python3 script to create playlist vids
"""

# youtube_dl
import youtube_dl

# args check
import argparse
import re
from os.path import exists

#utility (stderr)
import sys


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def parse_args() -> argparse.Namespace:
    """
        Parses arguments, yes
    :return: returns parsed arguments by argparse
    """
    parser = argparse.ArgumentParser(
        description="ytcp - YouTube Create Playlist video")
    parser.add_argument('--list', required=True, type=str,
                        help='source file for youtube audio links')
    parser.add_argument('--resolution',
                        type=str,
                        help='set resolution of the output video',
                        default='1280x720')
    parser.add_argument(
        '-o',  type=str, help='set output file name', default='output.mp4')
    parser.add_argument('--foreground-image', type=str,
                        help='set a custom image which will be displayed in the middle of the screen in the video')
    parser.add_argument('--background-image', required=True, type=str,
                        help='set a custom image which will fill the screen in the video')
    return parser.parse_args()


def check_args(args: argparse.Namespace):
    """
        Runs sanity checks for arguments and ends program exec if something is wrong.
    """
    if (args.foreground_image and not exists(args.foreground_image)):
        raise FileNotFoundError("foreground_image")

    if (args.background_image and not exists(args.background_image)):
        raise FileNotFoundError("background_image")

    if (args.list and not exists(args.list)):
        raise FileNotFoundError("list")

    if (not re.fullmatch('[0-9]{2,5}x[0-9]{2,5}', args.resolution)):
        raise ValueError("resolution")


if __name__ == "__main__":
    args = parse_args()
    try:
        check_args(args)
    except Exception as e:
        eprint("[ERR] : " + str(e.__class__) + " : " + str(e))

    resolution = args.resolution.split('x')

    resolution_w = resolution[0]
    resolution_h = resolution[1]
    bg_img = args.background_image
    fg_img = args.foreground_image
    list_file = args.list
