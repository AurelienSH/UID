import utils.metrics as m
import utils.conll2 as c2
import control_that2 as control_that
import pandas as pd
import csv
import uidDoublons
from transformers import BertTokenizer, BertModel
from transformers import GPT2Tokenizer, GPT2Model
import torch
import numpy as np

def get_taux_omit(conll):
    taux_omit = {}
    for sent in conll:
        for cc_head in sent.cc_heads:
            m_verb = control_that.get_matrix_verb(sent[cc_head.id], sent)
            lemma = m.get_lemma(m_verb, sent)
            taux_omit[lemma] = taux_omit.get(lemma,{"omit":0,"nomit":0})
            that_omission = abs(control_that.get_that(cc_head, sent) - 1)
            if that_omission:
                taux_omit[lemma]["omit"] += 1
            else:
                taux_omit[lemma]["nomit"] += 1

    for verb in taux_omit.keys():
        res = taux_omit[verb]["omit"] / (taux_omit[verb]["omit"] + taux_omit[verb]["nomit"])
        taux_omit[verb] = res

    return taux_omit


def get_data(sent, taux_omit,uid_dict, scores):
    sentData = []
    sentDict = {}
    i=0
    m_verbs = set()
    m_verb_to_id = {}
    for cc_head in sent.cc_heads:
        if uid_dict.get(f"{sent.id}_{i+1}", False):
            if cc_head.form != "_":
                m_verb = control_that.get_matrix_verb(sent[cc_head.id], sent)
                lemma = m.get_lemma(m_verb, sent)
                m_verbs.add(lemma)
                m_verb_to_id[lemma] = m_verb_to_id.get(lemma,len(m_verbs))
                if 0.0 < taux_omit[lemma] < 1.0 and abs_freq[lemma]>=10:
                    m_subj = control_that.get_matrix_subject(cc_head, sent)
                    cc_subj = control_that.get_CC_subject_availability(cc_head, sent)
                    that = control_that.get_that(cc_head, sent)
                    tmpdic = {
                        'matrix_subject1v2': (1 if m_subj==1 else 0),
                        'matrix_subject1v3': (1 if m_subj==2 else 0),
                        'matrix_subject1v4': (1 if m_subj==3 else 0),
                        'frequency_matrix_verb': control_that.get_frequency_matrix_verb(cc_head, sent, freq),
                        'word_form_similarity': control_that.get_word_sim(cc_head, sent),
                        'frequency_CC_subject_head': control_that.get_frequency_cc_subject_head(cc_head, freq, sent),
                        'subject_form_CC_subject1v2': (1 if cc_subj==1 else 0),
                        'subject_form_CC_subject1v3': (1 if cc_subj==2 else 0),
                        'subject_form_CC_subject1v4': (1 if cc_subj==3 else 0),
                        'position_matrix_verb': control_that.get_position_matrix_verb(cc_head, sent),
                        'length_CC_remainder': control_that.get_length_cc_remainder(cc_head, sent),
                        'length_CC_onset': control_that.get_length_cc_onset(cc_head, sent),
                        'length_matrix_verb_to_CC': control_that.get_start_matrix_verb_to_cc(cc_head, sent),
                        'that_omission': abs(that-1),
                        'm_verb': m_verb_to_id[lemma],
                        'uid_jaeger': uid[lemma]
                    }
                    for score in scores:
                        tmpdic[f"uid_{score}"]=uid_dict[f"{sent.id}_{i+1}"][score]
                    sentData.append(tmpdic)
                    sentDict[f"{sent.id}_{i+1}"]=tmpdic
                    sentDict[f"{sent.id}_{i+1}"]["text"]=sent.text
                    sentDict[f"{sent.id}_{i+1}"]["mverb"]=m_verb.form
                    
        i+=1
    return sentData, sentDict

def createData(data):
    # verbs = []
    # freq_ = []
    # omit = []
    # uid_ = []

    # for verb, om in taux_omit.items():
    #     if 0.0 < taux_omit[verb] < 1.0 and abs_freq[verb]>=10:
    #         verbs.append(verb)
    #         freq_.append(abs_freq.get(verb,0))
    #         omit.append(om)
    #         uid_.append(uid[verb])

    # pd.DataFrame({"lemme":verbs, "frequence": freq_, "taux d'omission": omit, "uid": uid_}).to_csv(f"bigreal{score}.csv")

    keys = set(data[0].keys())


    with open(f'../modeling/bert_gum_nofrac.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

def create_couple_scores(scores):
    l_scores = list(scores)
    couples_scores = []
    i = 0
    while i<len(l_scores)-1:
        j = i+1
        while j<len(l_scores):
            couples_scores.append((l_scores[i],l_scores[j]))
            j+=1
        i+=1
    return couples_scores

def explore_extrema(dataDict, couple_scores, filename):
    extrema = dict()
    with open(filename, "w") as f:
        for couple in couple_scores:
            extrema[couple]={"ecart": 0, "mverb": "NaN", "sent": "NaN"}
            for sent_cc_key in dataDict.keys():
                sent_cc = dataDict[sent_cc_key]
                ecartSent = abs(sent_cc[f"uid_{couple[0]}"] - sent_cc[f"uid_{couple[1]}"])
                ecartSaved = extrema[couple]["ecart"]
                if ecartSent>ecartSaved:
                    extrema[couple]["ecart"] = ecartSent
                    extrema[couple]["sent"] = sent_cc["text"]
                    extrema[couple]["mverb"] = sent_cc["mverb"]
                    extrema[couple][couple[0]] = sent_cc[f"uid_{couple[0]}"]
                    extrema[couple][couple[1]] = sent_cc[f"uid_{couple[1]}"]
    with open(filename, "w") as f:
        print("couple\tecart\ttexte\tscore1\tscore2", file=f)
        for couple in extrema.keys():
            print(f"{couple[0]}_{couple[1]}\t{extrema[couple]['ecart']}\tmverb : {extrema[couple]['mverb']}_{extrema[couple]['sent']}\t{extrema[couple][couple[0]]}\t{extrema[couple][couple[1]]}", file=f)

    return extrema

if __name__ == "__main__":
#    folder = '../Data/'
#    full_conll2 = c2.read_conll(f"{folder}GUM/all_GUM_SUD.conllu",f"{folder}all_GUM.conllu")
#    genres = c2.get_genres(full_conll2)
#    genres2id = {g:i for i, g in zip(range(len(genres)),genres)}
#    id2genres = {i:g for g, i in genres2id.items()}
#    cc_conll = c2.read_conll(f"{folder}GUM/CC_GUM/all_CC_SUD.conllu",f"{folder}CC_GUM/all_CC_UD.conllu")
#    freq, abs_freq = m.lemma_freq(full_conll2)
#    uid = m.uid_2010(full_conll2)


    folder = '../Data/GUM/'
    full_conll2 = c2.read_conll(f"{folder}all_GUM_SUD.conllu",f"{folder}all_GUM.conllu")
    genres = c2.get_genres(full_conll2)
    genres2id = {g:i for i, g in zip(range(len(genres)),genres)}
    id2genres = {i:g for g, i in genres2id.items()}
    freq, abs_freq = m.lemma_freq(full_conll2)
    uid = m.uid_2010(full_conll2)

    uid_df = pd.read_csv("scores_bert_gum_nofrac.tsv",sep="\t", index_col=0)
    uid_dict = uid_df.to_dict(orient='index')

    data = []
    dataDict = {}
    taux_omit = get_taux_omit(full_conll2)

    scores = set(uid_dict[list(uid_dict.keys())[0]].keys())



    for sud_sent in full_conll2:
        sentdata, sentDict = get_data(sud_sent, taux_omit, uid_dict, scores)
        if sentdata:
            data += sentdata
            dataDict.update(sentDict)

    scores.add("jaeger")
    
    couple_scores = create_couple_scores(scores)

    explore_extrema(dataDict, couple_scores,"extrema_exploration_bert_gum.tsv")
   
    createData(data)