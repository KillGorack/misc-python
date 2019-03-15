import os

mypath = "C:/Users/dmonr/Music"
f = []
for folder, subfolder, file in os.walk(mypath):
 for filename in file:
    f.append(os.path.join(folder,filename))


for songs in f:
    print(songs)
