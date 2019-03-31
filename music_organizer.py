from tinytag import TinyTag
import os
import sqlite3
import shutil
from random import randint
# =============================================
# Define paths (later use db relative)
# =============================================
path_error      = "//home//dave//Music//error"
path_read       = "//home//dave//Music//drop"
path_cleaned    = "//home//dave//Music//library"
path_data       = "//home//dave//Music//musical_data.db"
# =============================================
# Definition for checking paths
# =============================================
def check_paths(path_error, path_read, path_cleaned, path_data):
    rtrn = True
    if os.path.exists(os.path.dirname(os.path.abspath(path_data))) == False:
        rtrn = False
    if os.path.exists(path_error) == False:
        rtrn = False
    if os.path.exists(path_read) == False:
        rtrn = False
    if os.path.exists(path_cleaned) == False:
        rtrn = False
    return rtrn
# =============================================
# Definition for checking paths content
# =============================================
def check_content(path_error, path_cleaned):
    rtrn = True
    path, dirs, files = next(os.walk(path_error))
    if len(files) > 0:
        rtrn = False
    path, dirs, files = next(os.walk(path_cleaned))
    if len(files) > 0:
        rtrn = False
    return rtrn
# =============================================
# Database birth
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
# prestart check
# =============================================
def start_check(path_error, path_read, path_cleaned, path_data):
    stp = False
    msg = ""
    if(check_paths(path_error, path_read, path_cleaned, path_data) == False):
        msg = "One or more of the needed directories do not exist, check your py."
        stp = True
    if(check_content(path_error, path_cleaned) == False):
        msg = "One or more of the needed directories have files within, Delete from the error, and cleaned directories, as they need to be empty."
        stp = True
    return [stp, msg]
# =============================================
# A list of ALL files....
# =============================================
def getfiles(path_read):
    f = []
    for folder, subfolder, file in os.walk(path_read):
        for dbname in file:
            f.append(os.path.join(folder,dbname))
    return f
# =============================================
# Get musical data
# =============================================
def gather_data(file_list, path_data):
    cleaned = []
    duped = []
    error = []
    test = []
    err = 0
    conn = sqlite3.connect(path_data)
    c = conn.cursor()
    for song in file_list:
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
            comp = str(tag.album) + str(tag.albumartist) + str(tag.title) + str(tag.filesize) + str(tag.samplerate) + str(tag.bitrate)
            print(item)
            if(comp in test):
                duped.append(item)
            elif len(tag.album.strip()) == 0 or len(tag.albumartist.strip()) == 0 or len(tag.title.strip()) == 0:
                error.append(item)
            else:
                cleaned.append(item)
                test.append(comp)
                c.execute('insert into music_data(`album`,`albumartist`,`artist`,`audio_offset`,`bitrate`,`comment`,`disc`,`disc_total`,`duration`,`filesize`,`genre`,`samplerate`,`title`,`track`,`track_total`,`year`,`path`, ext) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', item)
        except:
            error.append(song)
    conn.commit()
    conn.close()
    return [cleaned, duped, error]
# =============================================
# Your basic cleaner
# =============================================
def string_cleaner(cleaned_string):
    bad_chars = ['~','#','%','*','(',')','[',']','{','}','/','/',':','?','|','\"','\'']
    for i in bad_chars:
        cleaned_string = cleaned_string.replace(i, '')
    return cleaned_string
# =============================================
# Move to cleaned area..
# =============================================
def move_to_cleaned(files, movepath):
    if(len(files) > 0):
        for file in files:
            dest = movepath + "/" + string_cleaner(file[1]) + "/" + string_cleaner(file[0]) + "/"
            newpath = dest + string_cleaner(file[12]) + " " + string_cleaner(file[17])
            if not os.path.exists(dest):
                os.makedirs(dest)
            shutil.copy(file[16], newpath)
        return True
    else:
        return False
# =============================================
# Duplicates
# =============================================
def move_to_dupes(files, movepath):
    if(len(files) > 0):
        for file in files:
            dest = movepath + "/" + string_cleaner(file[1]) + "/" + string_cleaner(file[0]) + "/"
            newpath = dest + string_cleaner(file[12]) + " " + string_cleaner(file[17])
            if not os.path.exists(dest):
                os.makedirs(dest)
            shutil.copy(file[16], newpath)
        return True
    else:
        return False
# =============================================
# error
# =============================================
def move_to_error(files, movepath):
    if(len(files) > 0):
        for file in files:
            if(len(file) <> 19):
                a=1
            else:
                dest = movepath + "/" + string_cleaner(file[1]) + "/" + string_cleaner(file[0]) + "/"
                newpath = dest + string_cleaner(file[12]) + " " + string_cleaner(file[17])
                if not os.path.exists(dest):
                    os.makedirs(dest)
                shutil.copy(file[16], newpath)
        return Truedd
    else:
        return False
# =============================================
# Do the thing
# =============================================
precheck = start_check(path_error, path_read, path_cleaned, path_data)
if precheck[0] == False:
    db_init(path_data)
    file_list = getfiles(path_read)
    inventory = gather_data(file_list, path_data)
    move_to_cleaned(inventory[0], path_cleaned)
    move_to_dupes(inventory[1], path_error)
    move_to_error(inventory[1], path_error)
