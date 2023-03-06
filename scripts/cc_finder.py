import pickle

with open("convDict.pkl","rb") as f:
    convDict = pickle.load(f)

def get_utt_str(utterance):
    return " ".join([token["text"] for token in utterance])
speaker_test = convD