#!/bin/python3
"""
    YTCP - python3 script to create playlist vids
"""

# youtube_dl
import youtube_dl
from multiprocessing.dummy import Pool as ThreadPool

# concat audio
# from moviepy.editor import concatenate_audioclips, AudioFileClip
import subprocess

# audio  length
from mutagen.mp3 import MP3


# clear parts folder
import os,  shutil

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
        # "restrictfilenames": True,
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


def clear_songs(folder : str):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder,filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed  to delete %s. Reason: %s' % (file_path, e))


# def absoluteFilePaths(directory):
#    for dirpath,_,filenames in os.walk(directory):
#        for f in filenames:
#            yield os.path.abspath(os.path.join(dirpath, f))

def relativeFilePaths(directory):
    for filename in os.listdir(directory):
        os.rename(os.path.join(directory, filename), os.path.join(directory, filename.replace('\'', '')))
    for filename in os.listdir(directory):
        yield ''.join([directory, filename])
# def concatenate_audio_moviepy(folder : str, output_path):
#     """Concatenates several audio files into one audio file using MoviePy
#     and save it to `output_path`. Note that extension (mp3, etc.) must be added to `output_path`"""
#
#
#     clips = [AudioFileClip(c) for c in absoluteFilePaths(folder)]
#     final_clip = concatenate_audioclips(clips)
#     final_clip.write_audiofile(output_path)

def concatenate_audio_ffmpeg(folder : str, output_path):
    """
        Concatenates several audio files into one audio file using ffmpeg
        and save ot to 'output_path'.
    """
    confile = "confiles.txt"
    clips = [("file '" + path + "'") for path in relativeFilePaths(folder)]
    with open(confile, "w") as f:
        f.write('\n'.join(clips) + '\n')
    os.system(f"ffmpeg -f concat -safe 0 -i {confile} -c copy -y {output_path}")

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

    clear_songs("parts/")
    fetch_songs(song_list)
    audio_concat = "out/audio.mp3"
    print('before')
    concatenate_audio_ffmpeg("parts/", audio_concat)
    print('after')
    audiolength_sec = MP3(audio_concat).info.length

    # TODO: Resolution support
    # TODO: -o support
    # TODO: Custom kbps choice

    os.system(f"ffmpeg -i {audio_concat} -f image2 -r 1/{audiolength_sec} -i {bg_img} -vcodec libx264 -y ./out/result.mp4")
