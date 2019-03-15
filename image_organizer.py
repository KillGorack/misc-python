import os
import os.path, time
from PIL import Image
from PIL.ExifTags import TAGS
import datetime, calendar, shutil, subprocess
# =================================================================
# Yea this it what this file does...
# =================================================================
# modify directories below in the "paths" section
# this will organize your images/photos by year and month..
# =================================================================
# paths...
# =================================================================
fromdir = "E:/Users/David/Pictures/_drop"
destdir = "E:/Users/David/Pictures/_organized"
errodir = "E:/Users/David/Pictures/_err"
stp = False
# =================================================================
# definitions
# =================================================================
def month_converter(month):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return months.index(month) + 1
# =================================================================
# main look that does the work..
# =================================================================
def movinator():
    for subdir, dirs, files in os.walk(fromdir):
      for file in files:
        filepath = subdir + os.sep + file
        try:
          dt = Image.open(filepath)._getexif()[36867]
          yr = dt[:4]
          mo = dt[5:7] + "_" + datetime.date(1900, int(dt[5:7]), 1).strftime('%B')
          dy = dt[8:10]
          pre = "photo_"
          path = destdir + "/" + yr + "/" + mo + "/" + str(int(dy)).zfill(2) + "/"
        except:
          try:
            dt = time.ctime(os.path.getmtime(filepath))
            yr = dt[-4:]
            moint = month_converter(dt[4:7])
            mo = str(moint).zfill(2) + "_" + datetime.date(1900, int(moint), 1).strftime('%B')
            dy = dt[8:10]
            pre = "image_"
            path = destdir + "/" + yr + "/" + mo + "/" + str(int(dy)).zfill(2) + "/"
          except:
            stp = True
            pre = "unknown_"
            path = errodir + "/"
        ext = os.path.splitext(file)[1]
        if not os.path.exists(path):
          os.makedirs(path)
        list = os.listdir(path)
        cnt = len(list) + 1
        shutil.move(subdir + "/" + file, path + pre + str(cnt).zfill(2) + ext)
# =================================================================
# Monitor
# =================================================================
movinator()
before = dict ([(f, None) for f in os.listdir (fromdir)])
while 1:
  time.sleep (10)
  after = dict ([(f, None) for f in os.listdir (fromdir)])
  added = [f for f in after if not f in before]
  removed = [f for f in before if not f in after]
  if added:
    print ("Files detected, calling for a file move..")
    movinator()
  before = after















    
