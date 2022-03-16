#!/bin/python3
"""
    YTCP - python3 script to create playlist vids
"""

import youtube_dl
import argparse


def parse_args():
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


if __name__ == "__main__":
    print(parse_args)
