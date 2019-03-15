from tinytag import TinyTag
import os
import sqlite3
# =============================================
# Get all music files into an array..
# =============================================
mypath = "C:/Users/dmonr/Music"
f = []
for folder, subfolder, file in os.walk(mypath):
    for filename in file:
        f.append(os.path.join(folder,filename))
# =============================================
# database birth
# =============================================
filename = 'e:/musical_data.db'
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
# =============================================
# Loop through the data and add stuff to the db
# =============================================
for song in f:
    try:
        tag = TinyTag.get(song)
        filename = 'e:\musical_data.db'
        conn = sqlite3.connect(filename)
        c = conn.cursor()
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
        conn.commit()
        conn.close()
    except:
        a = True
