from tinytag import TinyTag
import os
import sqlite3
import shutil
from random import randint
# =============================================
# Opening statements
# =============================================
def statement():
    print("This utility will find duplicates using meta data, and move them to a specified location")
    print("It uses album, artist, bitrate, samplerate, and filesize to compare.")
    print("Please see the paths section of this program and modify for your needs")
    print("The author of this script is NOT responsible for damage done to your computer, or music library.")
    input("Press enter to continue")
# =============================================
# Paths
# =============================================
musicpath = "C:\\Users\\David\\Music\\iTunes\\iTunes Media\\Music"
dbname = "C:\\Users\\David\\Music\\iTunes\\iTunes Media\\musical_data.db"
movepath = "C:\\Users\\David\\Music\\iTunes\\iTunes Media\\Moved"
organized = "C:\\Users\\David\\Music\\iTunes\\iTunes Media\\Cleaned"
# =============================================
# Get all music files into an array..
# =============================================
def getfiles(musicpath):
    f = []
    for folder, subfolder, file in os.walk(musicpath):
        for dbname in file:
            f.append(os.path.join(folder,dbname))
    return f
# =============================================
# database birth
# =============================================
def db_init(dbname):
    conn = sqlite3.connect(dbname, timeout=10)
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
    `path`              TEXT,
    `ext`               TEXT
    )''');
    c.execute("delete from 'music_data'");
    conn.commit()
    c.execute("delete from sqlite_sequence where name='music_data'");
    conn.commit()
    conn.close()
    return True
# =============================================
# Cram the data into the DB
# =============================================
def gather_data(f, dbname):
    md = []
    ed = []
    test = []
    err = 0
    conn = sqlite3.connect(dbname)
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
            song,
            os.path.splitext(song)[1]
            ]
            comp = ','.join([tag.album, tag.artist, tag.title, str(tag.filesize), str(tag.samplerate), str(tag.bitrate)])
            if(comp in test):
                ed.append(item)
            else:
                md.append(tag)
                test.append(comp)
                c.execute('insert into music_data(`album`,`albumartist`,`artist`,`audio_offset`,`bitrate`,`comment`,`disc`,`disc_total`,`duration`,`filesize`,`genre`,`samplerate`,`title`,`track`,`track_total`,`year`,`path`, ext) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', item)
        except:
            err = err + 1
    conn.commit()
    conn.close()
    return [err, len(md), ed]
# =============================================
# Just a function for whatever
# =============================================
def rand_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)
# =============================================
# move the found dupes..
# =============================================
def move_files(files, movepath):
    if(len(files) > 0):
        for file in files:
            dest = movepath + "\\" + file[2] + "\\" + file[0] + "\\"
            newpath = dest + file[12] + " " + str(rand_digits(12)) + file[17]
            try:
                os.makedirs(dest)
            except:
                a = a
            shutil.move(file[16], newpath)
            print(str(len(files)) + " Files moved.")
    else:
        print("no dupes found")
    return True
# =============================================
# do the thing
# =============================================
print(statement())
db = db_init(dbname)
filelist = getfiles(musicpath)
if db == True and len(filelist) > 0:
    results = gather_data(filelist, dbname)
    move_files(results[2], movepath)
