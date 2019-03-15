import os
import requests
from os import walk
import os.path, time
import numpy as np
import json

fromdir = "C:/Users/dmonr/Desktop/MOVER/_drop"
destdir = "C:/Users/dmonr/Desktop/MOVER/dest"
errodir = "C:/Users/dmonr/Desktop/MOVER/error"
fullurl = "http://localhost/portal-x/index.php?ala=test"

def movefiles():
  print("Moving files")

def parsefile(file):
  with open(file, 'r') as content_file:
    content = content_file.read()
    content = content.replace("$$", "$")
    content = content.replace("$\r\n", "")
    content = content.replace("$\n", "")
    content = content.replace("$\r", "")
    content = content.replace(" ", "")
    content = content.splitlines()
    cleaned = []
    r = 0
    for c in content:
      if  c.upper().startswith(('OUTPUT/F', 'F(', 'T(', 'FA(', 'TA(', 'DATE', 'TIME', 'MD(LFD_NR)', 'DI(MESSMITTEL)', 'PN(TEIL_NR)', 'PS(YMD1)', 'PS(KENN)')):
        cleaned.append(c)
    requests.post(fullurl, data = {'data':json.dumps(cleaned)})


def listfiles():
  f = []
  for dirpath, subdirs, files in os.walk(fromdir):
    for x in files:
      if x.endswith(".dmo"):
        parsefile(os.path.join(dirpath, x))


listfiles()
