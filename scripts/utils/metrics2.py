from collections import defaultdict, Counter
from numpy import log
import sys

# appending the parent directory path
sys.path.append('../')

# importing the methods
from control_that2 import get_matrix_verb

def lemma_freq(conll):
    count = 0
    absolute_freq = {}
    freq = {}
    for sent in conll:
        count += len(sent.sentence)
        for token in sent.sentence:
            absolute_freq[token.lemma] = absolute_freq.get(token.lemma,0)+1
    for k, v in absolute_freq.items():
        freq[k] = v/count

    return freq, absolute_freq

def get_lemma(m_verb, sent):
    if m_verb.upos == "VERB":
        return m_verb.lemma
    elif m_verb.lemma == "sure":
        return "make sure"
    elif m_verb.rel == "root":
        for tok in sent.sentence:
            if tok.gov == m_verb.id and tok.rel == "cop":
                return f"be {m_verb.lemma}"
    return f"{sent[m_verb.gov].lemma} {m_verb.lemma}"

def uid_2010(conll):
    uid_ddict = defaultdict(Counter)
    keys = set()
    for sentence in conll:
        for cc_head in sentence.cc_heads:
            m_verb = get_matrix_verb(sentence[cc_head.id], sentence)
            lemma = get_lemma(m_verb, sentence)
            keys.add(lemma)
    for sentence in conll:
        for token in set(sentence.sentence):
            cc = False
            lemma = get_lemma(token, sentence)
            if lemma in keys:
                for cc_head in sentence.cc_heads:
                    if cc_head.gov == token.id:
                        cc =True
                if cc:
                    uid_ddict[lemma]["cc"]+=1
                else:
                    uid_ddict[lemma]["nocc"]+=1

    uid_dict = {}


    for lemma in uid_ddict.keys():
        cc = uid_ddict[lemma].get('cc', False)
        nocc = uid_ddict[lemma].get('nocc', False)
        if cc and nocc:
            uid_dict[lemma] = -log(cc / (cc + nocc))
        elif cc:
            uid_dict[lemma] = 0
        else:
            uid_dict[lemma] = 10

    return uid_dict

def create_dfs():
    return

