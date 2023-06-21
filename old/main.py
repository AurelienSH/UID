import csv
import pandas as pd
import sys
import glob as glb
import re
import pickle

callname_from_file_regex = re.compile(r".+/.+/sw(.+?)(A|B)")
utterance_from_file_regex = re.compile(r".+(\d{4})")
SpeakerToSentRegex = re.compile(r"^(\d{4}).+A_(\d{4}).+B_(\d{4})")
def giveMetadataToConvDict(file, convDict):
    with open(file, "r") as f:
        caller_csvreader = csv.reader(f)
        header = next(caller_csvreader)
        for row in caller_csvreader:
            if convDict.get(row[0], False):
                for k, v in zip(header[1:], row[1:]):
                    convDict[row[0]][k] = v
    return convDict

def makeConvDict(folder, speakerToConvDict):
    files = glb.glob(f"{folder}/*/*")
    convDict = {}
    for file in files :
        m = re.match(callname_from_file_regex, file)
        callname = m.group(1)
        sentences, speakerAB = getSentencesAndSpeakerFromFile(file)
        speaker = speakerToConvDict[callname][speakerAB]
        convDict[speaker] = convDict.get(speaker,{'conversations': {}})
        convDict[speaker]['conversations'][callname] = sentences
    return convDict

def getSentencesAndSpeakerFromFile(file):
    with open(file,"r") as f:
        conv = pd.read_csv(f, sep="\t", header = None)
        utterance_no = None
        utterances = []
        utterance = []
        for line in conv.iterrows():
            m = re.match(utterance_from_file_regex, line[1][0])
            if utterance_no != m.group(1):
                if utterance:
                    utterances.append(utterance)
                utterance = []
                utterance_no = m.group(1)
            utterance.append({'text': line[1][6],'duration': float(line[1][3])-float(line[1][2])})
        speaker = "A" if ("A" in line[1][1]) else "B"
    return utterances, speaker

def makeSpeakerToConvDict(file):
    speakerToConvDict = {}
    with open(file, "r") as f:
        l = f.readline()
        while l:
            m = re.match(SpeakerToSentRegex, l)
            callname = m.group(1)
            speaker_A = m.group(2)
            speaker_B = m.group(3)
            speakerToConvDict[callname] = {"A": speaker_A, "B": speaker_B}
            l = f.readline()
    return speakerToConvDict

def main():
    convFolder = sys.argv[1]
    callerTab = sys.argv[2]
    summary = sys.argv[3]
    speakerToConvDict = makeSpeakerToConvDict(summary)
    convDict = makeConvDict(convFolder, speakerToConvDict)
    giveMetadataToConvDict(callerTab, convDict)
    with open("convDict.pkl","wb") as dump:
        pickle.dump(convDict,dump)
if __name__ == "__main__":
    main()