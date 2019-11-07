from pydub import AudioSegment
import os

_SECOND = 1000


def change_dB_Level(sound, level):
    difference = level - sound.dBFS
    return sound.apply_gain(difference)


outputDirectory = "./sound dataset/noisys/"
cleanDirectory = "./sound dataset/clean/"
noiseDirectory = "./sound dataset/noise/"
noisePath = ["subway"]
clearSounds = list()
noiseSounds = list()
clearSoundFile = noiseSoundFile = None
UPdBs = [3]
clearSoundCount = len(os.listdir(cleanDirectory))
noiseSoundCount = 0
for filename in os.listdir(cleanDirectory):
    clearSounds.append(filename)
for path in noisePath:
    noiseSoundCount += len(os.listdir(noiseDirectory+path))
    for filename in os.listdir(noiseDirectory+path):
        noiseSounds.append([path,  filename])
outputFileCount = noiseSoundCount*clearSoundCount*len(UPdBs)
finishCount = 0
for clearSound in clearSounds:
    clearSoundFile = AudioSegment.from_file(cleanDirectory+clearSound)
    clearLength = len(clearSoundFile)
    for noiseSound in noiseSounds:
        if noiseSound[1][-3:] == "mp3":
            noiseSoundFile = AudioSegment.from_mp3(
                noiseDirectory+noiseSound[0]+"/"+noiseSound[1])
        else:
            noiseSoundFile = AudioSegment.from_file(
                noiseDirectory+noiseSounds[0]+"/"+noiseSound[1])
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
                outputDirectory + noiseSound[0]+noiseSound[1][0:-4]+"_" + clearSound + "_"+str(UPdB)+"dB.wav")
            print("{:.4}%\tfinished ".format(str(finishCount/outputFileCount)) + noiseSound[0]+noiseSound[1]
                  [0:-4]+"_" + clearSound + "_"+str(UPdB)+"dB.wav")
