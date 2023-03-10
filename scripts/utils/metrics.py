from collections import defaultdict, Counter
from numpy import log

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

    return freq

def uid_2010(conll):
    uid_dict = defaultdict(Counter)
    for sentence in conll:
        for gov in set(sentence.sentence):
            cc = False
            if gov.upos == "VERB":
                for dep in set(sentence.sentence):
                    if dep.gov == gov.id:
                        if dep.upos == "VERB" and dep.rel == "ccomp":
                            cc = True
                if cc:
                    uid_dict[gov.lemma]['cc'] += 1
                else:
                    uid_dict[gov.lemma]['nocc'] += 1

    uid_dict = {k: dict(v) for k, v in dict(uid_dict).items()}

    final_uid_dict = {}

    for lemma in uid_dict.keys():
        cc = uid_dict[lemma].get('cc', False)
        nocc = uid_dict[lemma].get('nocc', False)
        if cc and nocc:
            final_uid_dict[lemma] = -log(cc / (cc + nocc))
        elif cc:
            final_uid_dict[lemma] = 0
        else:
            final_uid_dict[lemma] = 10

    return final_uid_dict