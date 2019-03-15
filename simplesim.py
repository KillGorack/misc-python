import random
import os
import time
import sqlite3
import tkinter

# =============================================================
# Create a DB with a table..
# =============================================================
filename = 'e:\data.db'
conn = sqlite3.connect(filename, timeout=10)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS `simdata` (`ID`  INTEGER PRIMARY KEY AUTOINCREMENT, `sim_steps`   TEXT, `sim_eaten`   INTEGER)''');
conn.close()
# =============================================================
# main Loop. Yea it's all one big loop thing..
# =============================================================
record = 0
count = 0
for x in range(0, 10000):
  if count >= record:
    record = count
  sz = 10
  fd = 3
  fax = []
  fay = []
  fal = []
  for x in range(0, int(fd)):
      szx = random.randint(1, int(sz))
      szy = random.randint(1, int(sz))
      fax.extend([szx])
      fay.extend([szy])
      fal.extend(["false"])
  # ===========================================================
  # Lets place our person somewhere..
  # ===========================================================
  px = random.randint(1, int(sz))
  py = random.randint(1, int(sz))
  #print("Your dude starts at position: " + str(px) + ", " + str(py) + ".")
  # ===========================================================
  # Set some variables to begin with..
  # ===========================================================
  health = 100
  count = 0
  # ===========================================================
  # The main Loop where we move around.
  # ===========================================================
  while health > 0:
      # =======================================================
      # Lets decide which way to move!
      # =======================================================
      mx = random.randint(0, 7)
      if mx == 0:
          px = px + 1
      if mx == 1:
          px = px + 1
          py = py + 1
      if mx == 2:
          py = py + 1
      if mx == 3:
          px = px - 1
          py = py + 1
      if mx == 4:
          px = px - 1
      if mx == 5:
          px = px - 1
          py = py - 1
      if mx == 6:
          py = py - 1
      if mx == 7:
          px = px + 1
          py = py - 1
      if int(px) > int(sz):
          px = int(sz)
      if int(px) < 1:
          px = 1
      if int(py) > int(sz):
          py = int(sz)
      if int(py) < 1:
          py = 1
      # =======================================================
      # Find some health? lets eat, and go on!
      # =======================================================
      q = 0
      while q < len(fax):
          if fax[q] == px and fay[q] == py and fal[q] == "false":
              print ("Found some health!")
              health = 100
              fal[q] = "true"
          q += 1
      # =======================================================
      # It takes some energy to move forward!
      # =======================================================
      health -= 1
      # =======================================================
      # Lets count our steps..
      # =======================================================
      # print("@ position: " + str(px) + ", " + str(py) + ",@ " + str(health))
      count = int(count)
      count += 1
  # ===========================================================
  # Death comes for us all..
  # ===========================================================
  print ("You have died after taking " + str(count) + " steps.")
  # ===========================================================
  # Lets save some data..
  # ===========================================================
  h = 0
  hc = 0
  while h < len(fal):
      if fal[h] == "true":
          hc = hc + 1
      h += 1
  filename = 'e:\data.db'
  conn = sqlite3.connect(filename)
  c = conn.cursor()
  item = [(str(count)), (hc)]
  c.execute('insert into simdata(`sim_steps`, `sim_eaten`) values (?, ?)', item)
  conn.commit()
  conn.close()
  #time.sleep(2)
# =============================================================
# the final result
# =============================================================
print ("Your record is: " + str(record) + ".")
