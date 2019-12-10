from gtts import gTTS
import os, sys, glob
import pyo
import keyboard
import csv

language = 'en'

keybinds = []
with open("keybinds.tsv") as fd:
    rd = csv.reader(fd, delimiter='\t', quotechar='"')
    for row in rd:
        key = row[0]
        text = row[1]
        filename = "text_" + key
        keybinds.append((key,filename + ".aif"))
        print("Loading %s... [%s]" % (key, text))

        output = gTTS(text=text, lang=language, slow=False)
        output.save(filename + ".mp3")
        
        os.system("ffmpeg -hide_banner -loglevel panic -y -i %s.mp3 %s.aif" % (filename, filename))
        os.remove(filename + ".mp3")

s = pyo.Server()
s.boot().start()

sf_players = dict()
for key, filename in keybinds:
    sf_players[key] = pyo.SfPlayer(path=filename, mul=0.5)

def play_file(key):
    print(key)
    sf_players[key].out()

running = True
def stop():
    global running
    running = False

for key, _ in keybinds:
    keyboard.add_hotkey(key, play_file, args=(key,))

keyboard.add_hotkey('esc', stop)

while True:
    if not running:
        break

#for f in glob.glob("*.aif"): os.remove(f)