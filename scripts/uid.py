from collections import defaultdict, Counter
from numpy import log

def get_uid_2010(conll):
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

    return final_uid_dict