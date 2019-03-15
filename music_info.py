import magic
import eyed3


audiofile = eyed3.load("C:/Users/dmonr/Music/Deee-Lite/World Clique/09 Groove is in the heart.mp3")
print (audiofile.tag.artist)
print (audiofile.tag.album)
print (audiofile.tag.title)
print (audiofile.tag.track_num)
print (audiofile.tag.genre)
