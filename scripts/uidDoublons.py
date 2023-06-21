from transformers import BertTokenizer, BertModel
from transformers import GPT2Tokenizer, GPT2Model
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import numpy as np
import utils.conll2 as c2
import pandas as pd

model = AutoModelForCausalLM.from_pretrained("gpt2")
tokenizer = AutoTokenizer.from_pretrained("gpt2")

generated_that = 0
generated_om = 0


def get_probs_from_sent(sentence):

    input_ids = tokenizer.encode(sentence, return_tensors='pt')

    with torch.no_grad():
        logits = model(input_ids=input_ids).logits

    probabilities = logits.softmax(dim=-1).tolist()[0]

    probs = []

    for i, token in enumerate(tokenizer.tokenize(sentence)):
        probs.append(max(probabilities[i]))


    return probs


def generate_doublon(sent, cc_head):
    global generated_om
    global generated_that
    sentList = [token.form for token in sent.ud]
    marks = sent.get_deps(cc_head, "mark")
    tmp = [mark.id for mark in marks if mark.form == "that"]
    if tmp:
        that_i = [mark.id for mark in marks if mark.form == "that"][0] - 1
        if that_i:
            generated_om += 1
            sentListBis = sentList[:that_i]+sentList[that_i+1:]
            return {"nothat": sentListBis, "that":sentList}

    that_i = sent[sent.get_first_token_of_clause(cc_head)].id
    if sent[that_i-1].upos == "VERB":
        sentListBis = sentList[:that_i-1]+["that"]+sentList[that_i-1:]
        generated_that +=1
        return {"that": sentListBis, "nothat":sentList}
    return None


def get_lambda_i(that, nothat):
    i=0
    for k, l in zip(that, nothat):
        if k!=l:
            return (i+1)
        i+=1
    return None

def UID_var(list):
    return (-np.var(list))


def UID_theta(lis, n, lambda_i):
    return np.mean(lis[lambda_i:(lambda_i + n)])


def UID_igauche(list, theta, k, lambda_i):
    igauche = np.mean(list[(lambda_i - k):lambda_i])
    return (-np.abs(theta - igauche))


def UID_iphrase(list, theta):
    iphrase = np.mean(list)
    return (-np.abs(theta - iphrase))

def get_idoc(doc):
    """
    :param doc:
    :param model_name:
    :param format: peut etre "logits" ou "probabilities", ce sera la valeur à utiliser
    :return:
    """
    mean_sum = 0
    l=len(doc)
    for i, sent in enumerate(doc):
        print(f"{i}/{l}")
        mean_sum += np.mean(get_probs_from_sent(sent.text))

    return mean_sum/l

def UID_idoc(theta):
    global idoc
    return (-np.abs(theta-idoc))


def UID_biggestStep(list):
    return (-np.max([np.abs(list[i] - list[i + 1]) for i in range(len(list) - 1)]))


def UID_amplitude(list):
    return (-np.abs(np.max(list) - np.min(list)))


def UID_avgStep(list):
    return (-np.mean([np.abs(list[i] - list[i + 1]) for i in range(len(list) - 1)]))

def generate_score_dict(doublon):
    probthat = get_probs_from_sent(" ".join(doublon["that"]))
    probnothat = get_probs_from_sent(" ".join(doublon["nothat"]))
    lambda_i = get_lambda_i(probthat, probnothat)
    var = UID_var(probthat)-UID_var(probnothat)
    amp = UID_amplitude(probthat)-UID_amplitude(probnothat)
    theta_that = UID_theta(probthat, 2, lambda_i)
    theta_nothat = UID_theta(probnothat, 2, lambda_i)
    igauche = UID_igauche(probthat, theta_that, 2, lambda_i)-UID_igauche(probnothat, theta_nothat, 2, lambda_i)
    iphrase = UID_iphrase(probthat, theta_that)-UID_iphrase(probnothat, theta_nothat)
    idoc = UID_idoc(theta_that)-UID_idoc(theta_nothat)
    biggestStep = UID_biggestStep(probthat)-UID_biggestStep(probnothat)
    avgStep = UID_avgStep(probthat)-UID_avgStep(probnothat)
    return {"var": var, "amp": amp, "igauche2_2": igauche, "idoc": idoc, "iphrase": iphrase, "biggestStep":biggestStep, "avgStep": avgStep}

def illustrate_scores(probs):
    lambda_i = 2
    dico = dict()
    theta = UID_theta(probs, 2, lambda_i)
    dico["var"] = UID_var(probs)
    dico["amp"] = UID_amplitude(probs)
    dico["theta"] = UID_theta(probs, 2, lambda_i)
    dico["igauche"] = UID_igauche(probs, theta, 2, lambda_i)
    dico["iphrase"] = UID_iphrase(probs, theta)
    dico["idoc"] = UID_idoc(theta)
    dico["biggestStep"] = UID_biggestStep(probs)
    dico["avgStep"] = UID_avgStep(probs)
    return dico

def justidoc(doublon):

    probthat = get_probs_from_sent(" ".join(doublon["that"]))
    probnothat = get_probs_from_sent(" ".join(doublon["nothat"]))
    lambda_i = get_lambda_i(probthat, probnothat)
    theta_that = UID_theta(probthat, 2, lambda_i)
    theta_nothat = UID_theta(probnothat, 2, lambda_i)
    idoc = UID_idoc(theta_that)-UID_idoc(theta_nothat)
    return idoc 

def createScoresDataframe(full_conll):
    doub_dict = {}
    l = len(full_conll)
    for j, sent in enumerate(full_conll):
        print(f"{j}/{l}")
        for i, cc_head in enumerate(sent.cc_heads):
            print("generating doublon")
            doub = generate_doublon(sent, cc_head)
            if doub:
                doub_scores = generate_score_dict(doub)
                doub_dict[f"{sent.id}_{i+1}"]=doub_scores

    df = pd.DataFrame.from_dict(data=doub_dict, orient='index')
    df.to_csv("scores_gpt_gum_nofrac.tsv", sep="\t")
    return doub_dict


if __name__ == "__main__":

    full_conll = c2.read_conll("../Data/GUM/all_GUM_SUD.conllu","../Data/GUM/all_GUM.conllu")

    with open("idocGUM","r") as f:    
        idoc = float(f.readline().strip())

    createScoresDataframe(full_conll)

    print(generated_that)
    print(generated_om)

    

    # that = "I believe that it isn't a bird.".split(" ")
    # nothat = "I believe it isn't a bird.".split(" ")
    # doublon = {"that": that, "nothat": nothat}

    # bigdico = generate_score_dict({"that": that, "nothat": nothat})

    # probthat = get_probs_from_sent(" ".join(doublon["that"]))
    # probnothat = get_probs_from_sent(" ".join(doublon["nothat"]))
    # print(f"prob that : {probthat}")
    # thatdico = illustrate_scores(probthat)
    # print(f"metriques that : {thatdico}")
    # print(f"prob nothat : {probnothat}")
    # nothatdico = illustrate_scores(probnothat)
    # print(f"metriques nothat : {nothatdico}")
    # print(f"valeurs de score final : {bigdico}")

