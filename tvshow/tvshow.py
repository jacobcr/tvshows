#!/usr/bin/env python
import csv
from os import path, listdir, makedirs
from os.path import basename
from shutil import move
import re


download = "/Users/jacobcr/Downloads"
tvshows = "/Users/jacobcr/Movies/tvshows"
extensions = ['avi', 'srt', 'mov', 'mkv', 'mp4']
relist = [re.compile("(\d+).(\d+)")]


def checkpath(folder):
    if not path.exists(folder):
        raise ValueError("Directory %s not exists" % folder)


def seasoncap(filepath):
    for rex in relist:
        result = rex.findall(filepath)
        if result and len(set(result)) == 1 and result[0][1]:
            result = set(result)
            seasoncap = result.pop()
            return seasoncap[0].zfill(2), seasoncap[1].zfill(2)

    print "Could not get season from %s" % filepath
    return None, None


def show(f, shows):
    for s in shows:
        for acr in s:
            if f.lower().count(acr):
                return s[0]


def downloaded(download_path, shows):
    for f in listdir(download_path):
        file_path = path.join(download_path, f)
        if path.isdir(file_path):
            downloaded(download_path, shows)  # recursive call
        elif file_path[-3:] in extensions:
            s = show(file_path, shows)
            if s:
                season, cap = seasoncap(file_path)
                if season and cap:
                    yield (s, season, cap, file_path)


def destination_dirs(filelist):
    showsdetected = set([(x[0], x[1]) for x in filelist])
    for show, season in showsdetected:
        showpath = path.join(tvshows, show)
        seasonpath = path.join(showpath, season)

        if not path.exists(showpath):
            print "Creating new directory for show %s" % show
            makedirs(showpath)

        if not path.exists(seasonpath):
            print "Creating directory for show %s season %s" % (show, season)
            makedirs(seasonpath)


def copyfiles(filelist):
    for file in filelist:
        filename = "%s_S%sE%s.%s" % (file[0], file[1], file[2], file[3][-3:])
        filepath = path.join(tvshows, file[0], file[1], filename)
        if path.exists(filepath):
            print "Already exists %s %s" % (filename, basename(file[3]))
            continue

        print filename
        move(file[3], filepath)


def loader(resource_path):
    with open(resource_path, 'r') as csvfile:
        for row in csv.reader(csvfile):
            yield row  # first value will be the folder name


def main():
    checkpath(download)
    checkpath(tvshows)
    shows = list(loader('tvshow.csv'))
    detected = list(downloaded(download, shows))

    destination_dirs(detected)
    copyfiles(detected)

if __name__ == "__main__":
    main()
