#!/bin/python3
"""
    YTCP - python3 script to create playlist vids
"""

# youtube_dl
import youtube_dl
from multiprocessing.dummy import Pool as ThreadPool

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
    parser.add_argument('--list', type=str,
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


def parse_file_list(filename: str) -> list:
    res = []
    with open(filename) as f:
        res = f.read().splitlines()
    return res


def speed_check(s):
    speed = s.get('speed')
    ready = s.get('downloaded_bytes', 0)
    total = s.get('total_bytes', 0)

    if speed and speed <= 77 * 1024 and ready >= total * 0.1:
        # if the speed is less than 77 kb/s and we have
        # at least one tenths of the video downloaded
        raise Exception('Abnormal downloading speed drop.')



def fetch_songs(songs: list):
    """
        Downloads audios from songs list
    """
    ydl_opts = {
        "noplaylist": True,
        "vcodec": None,
        "outtmpl": "parts/%(title)s.%(ext)s",
        # "listformats": True,
        # "simulate": True,
        "format": "bestaudio",
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }
    external_downloader = 'aria2c'
    if external_downloader:
        ydl_opts['external_downloader'] = external_downloader
        ydl_opts['external_downloader_args'] = ['-c', '-j 3', '-x 3', '-s 3', '-k 1M']
        # ydl_opts['buffersize'] = 3
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        # ydl.add_progress_hook(speed_check)
        # kind of done: Issue - deal with low download speed
        with ThreadPool() as pool:
            superlist = [[song] for song in songs]
            result = pool.map(ydl.download, superlist)
            print("[LOG] : Download complete!")

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
    song_list = parse_file_list(args.list)

    fetch_songs(song_list)
