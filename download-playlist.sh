#!/bin/sh
youtube-dl --extract-audio --audio-format mp3 -o "%(title)s.%(ext)s" $1
