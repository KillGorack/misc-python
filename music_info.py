from tinytag import TinyTag
import os
import sqlite3
import numpy as np
mypath = "C:\\Users\\dmonr\\Music"
filename = "e:\\musical_data.db"
# =============================================
# Get all music files into an array..
# =============================================
def getfiles(mypath):
    f = []
    for folder, subfolder, file in os.walk(mypath):
        for filename in file:
            f.append(os.path.join(folder,filename))
    return f
# =============================================
# database birth
# =============================================
def db_init(filename):
    conn = sqlite3.connect(filename, timeout=10)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS `music_data`
    (
    `ID`  INTEGER PRIMARY KEY AUTOINCREMENT,
    `album`             TEXT,
    `albumartist`       TEXT,
    `artist`            TEXT,
    `audio_offset`      TEXT,
    `bitrate`           TEXT,
    `comment`           TEXT,
    `disc`              TEXT,
    `disc_total`        TEXT,
    `duration`          TEXT,
    `filesize`          TEXT,
    `genre`             TEXT,
    `samplerate`        TEXT,
    `title`             TEXT,
    `track`             TEXT,
    `track_total`       TEXT,
    `year`              TEXT,
    `path`              TEXT
    )''');
    conn.close()
    return True
# =============================================
# Cram the data into the DB
# =============================================
def gather_data(f, filename):
    md = []
    err = 0
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    for song in f:
        try:
            tag = TinyTag.get(song)
            item = [
            tag.album,
            tag.albumartist,
            tag.artist,
            tag.audio_offset,
            tag.bitrate,
            tag.comment,
            tag.disc,
            tag.disc_total,
            tag.duration,
            tag.filesize,
            tag.genre,
            tag.samplerate,
            tag.title,
            tag.track,
            tag.track_total,
            tag.year,
            song
            ]
            c.execute('insert into music_data(`album`,`albumartist`,`artist`,`audio_offset`,`bitrate`,`comment`,`disc`,`disc_total`,`duration`,`filesize`,`genre`,`samplerate`,`title`,`track`,`track_total`,`year`,`path`) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', item)
            md.append(tag)
        except:
            err = err + 1
    conn.commit()
    conn.close()
    return [err, len(md)]
# =============================================
# do the thing
# =============================================
db = db_init(filename)
filelist = getfiles(mypath)
if db == True and len(filelist) > 0:
    print(gather_data(filelist, filename))
