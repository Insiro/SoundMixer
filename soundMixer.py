from pydub import AudioSegment
import os
import json


def change_dB_Level(sound, level):
    difference = level - sound.dBFS
    return sound.apply_gain(difference)


originSoundFile = additionSoundFile = None
outputFileDir = originalFileDir = addFileDir = ""
UPdBs = list()
originSounds = list()
additionSounds = list()
ADDPath = list()
mixtype = 0
with open("./config.json")as config:
    data = json.load(config)
    UPdBs = data["dB"]
    outputFileDir = data["outputPath"]
    originalFileDir = data["originPath"]
    addFileDir = data["addPath"]
    ADDPath = data["AddCategory"]
    mixtype = data["mixType"]

asd = True
if(outputFileDir == ""):
    print("outputFileDir is not defined")
    asd = False
if (originalFileDir == ""):
    asd = False
    print("originalFileDir is not defined")
if (addFileDir == ""):
    asd = False
    print("addFileDir is not defined")
assert asd
assert len(ADDPath) != 0
assert len(UPdBs) != 0


outputFileCount = 0
for filename in os.listdir(originalFileDir):
    originSounds.append(filename)
for path in ADDPath:
    outputFileCount += len(os.listdir(addFileDir+path))
    for filename in os.listdir(addFileDir+path):
        additionSounds.append([path,  filename])
outputFileCount = outputFileCount*len(os.listdir(originalFileDir))*len(UPdBs)
finishCount = 0
for originSound in originSounds:
    originSoundFile = AudioSegment.from_file(originalFileDir+originSound)
    originLength = len(originSoundFile)
    for additionSound in additionSounds:
        if additionSound[1][-3:] == "mp3":
            additionSoundFile = AudioSegment.from_mp3(
                addFileDir+additionSound[0]+"/"+additionSound[1])
        else:
            additionSoundFile = AudioSegment.from_file(
                addFileDir+additionSounds[0]+"/"+additionSound[1])
        additionLength = len(additionSoundFile)
        if mixtype == -1:
            if additionLength > originLength:
                originSoundFile = originSoundFile * \
                    int(additionLength / originLength)
        elif mixtype == 1:
            if additionLength < originLength:
                additionSoundFile = additionSoundFile * \
                    int(originLength / additionLength)
        for UPdB in UPdBs:
            # control dB
            combineSound = change_dB_Level(
                additionSoundFile, UPdB).overlay(originSoundFile)
            # output wav
            finishCount += 1
            combineSound.export(
                outputFileDir + additionSound[0] + additionSound[1][0:-4]+"_" + originSound + "_" + str(UPdB)+"dB.wav")
            print("{:.4}%\tfinished ".format(str(finishCount/outputFileCount)) + additionSound[0]+additionSound[1]
                  [0:-4]+"_" + originSound + "_"+str(UPdB)+"dB.wav")
