from gtts import gTTS
import os, sys, glob
import pyo
import keyboard
import csv

language = 'en'

keybinds = dict()
with open("keybinds.tsv") as fd:
    rd = csv.reader(fd, delimiter='\t', quotechar='"')
    for row in rd:
        key = row[0]
        text = row[1]
        filename = "text_" + key
        keybinds[key] = filename + ".aif"
        print("Loading %s... [%s]" % (key, text))

        output = gTTS(text=text, lang=language, slow=False)
        output.save(filename + ".mp3")
        
        os.system("ffmpeg -hide_banner -loglevel panic -y -i %s.mp3 %s.aif" % (filename, filename))
        os.remove(filename + ".mp3")

s = pyo.Server(nchnls=2)
s.boot().start()

sf_players = (pyo.SfPlayer(path='text_q.aif', mul=0.5), pyo.SfPlayer(path='text_q.aif', mul=0.5))
def play_file(key):
    print("playing " + key)
    sf_players[0].setSound(keybinds[key])
    sf_players[1].setSound(keybinds[key])
    sf_players[0].out(0)
    sf_players[1].out(1)

running = True
def stop():
    global running
    running = False

for key in keybinds:
    keyboard.add_hotkey(key, play_file, args=(key,))

keyboard.add_hotkey('esc', stop)

while True:
    if not running:
        break

#for f in glob.glob("*.aif"): os.remove(f)