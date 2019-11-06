from pydub import AudioSegment
import os


def change_dB_Level(sound, level):
    difference = level - sound.dBFS
    return sound.apply_gain(difference)


directory = "./sound dataset"
noisePath = ["/noise"]
clearPath = "/clean long"
clearSounds = list()
noiseSounds = list()
clearSoundFile = noiseSoundFile = None
UPdBs = [3]
for filename in os.listdir(directory+clearPath):
    clearSounds.append(filename)
for path in noisePath:
    for filename in os.listdir(directory+path):
        noiseSounds.append([path,  filename])

for clearSound in clearSounds:
    clearSoundFile = AudioSegment.from_file(directory+clearPath+"/"+clearSound)
    for noiseSound in noiseSounds:
        if noiseSound[1][-3:] == "mp3":
            noiseSoundFile = AudioSegment.from_mp3(
                directory+noiseSound[0]+"/"+noiseSound[1])
        else:
            noiseSoundFile = AudioSegment.from_file(
                directory+noiseSounds[0]+"/"+noiseSound[1])
        for UPdB in UPdBs:
            combineSound = change_dB_Level(
                noiseSoundFile, UPdB).overlay(clearSoundFile)
            combineSound.export(
                directory+"/noisys/" + clearSound+"_"+noiseSound[1] + "_"+str(UPdB)+"dB.wav")
