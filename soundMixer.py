from pydub import AudioSegment
import os


def change_dB_Level(sound, level):
    difference = level - sound.dBFS
    return sound.apply_gain(difference)


UPdBs = list()
clearSounds = list()
noiseSounds = list()
clearSoundFile = noiseSoundFile = None
noisePath = list()
_OUT_DIR = "./sound dataset/noisy/"
_CLREN_DIR = "./sound dataset/clean/"
_NOISE_DIR = "./sound dataset/noise/"
with open("./noiseClass.txt")as fp:
    while True:
        line = fp.readline()
        if line == "":
            break
        noisePath.append(line)
assert len(noisePath) != 0
with open("./dBClass.txt")as fp:
    while True:
        line = fp.readline()
        if line == "":
            break
        UPdBs.append(int(line))
assert len(UPdBs) != 0

outputFileCount = 0
for filename in os.listdir(_CLREN_DIR):
    clearSounds.append(filename)
for path in noisePath:
    outputFileCount += len(os.listdir(_NOISE_DIR+path))
    for filename in os.listdir(_NOISE_DIR+path):
        noiseSounds.append([path,  filename])
outputFileCount = outputFileCount*len(os.listdir(_CLREN_DIR))*len(UPdBs)
finishCount = 0
for clearSound in clearSounds:
    clearSoundFile = AudioSegment.from_file(_CLREN_DIR+clearSound)
    clearLength = len(clearSoundFile)
    for noiseSound in noiseSounds:
        if noiseSound[1][-3:] == "mp3":
            noiseSoundFile = AudioSegment.from_mp3(
                _NOISE_DIR+noiseSound[0]+"/"+noiseSound[1])
        else:
            noiseSoundFile = AudioSegment.from_file(
                _NOISE_DIR+noiseSounds[0]+"/"+noiseSound[1])
        noiseLength = len(noiseSoundFile)
        multi = int(noiseLength/clearLength)if(noiseLength >
                                               clearLength) else 1
        for UPdB in UPdBs:
            # control dB
            combineSound = change_dB_Level(
                noiseSoundFile, UPdB).overlay(clearSoundFile*multi)
            # output wav
            finishCount += 1
            combineSound.export(
                _OUT_DIR + noiseSound[0]+noiseSound[1][0:-4]+"_" + clearSound + "_"+str(UPdB)+"dB.wav")
            print("{:.4}%\tfinished ".format(str(finishCount/outputFileCount)) + noiseSound[0]+noiseSound[1]
                  [0:-4]+"_" + clearSound + "_"+str(UPdB)+"dB.wav")
