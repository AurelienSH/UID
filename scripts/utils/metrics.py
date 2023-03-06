def lemma_freq(conll):
    count = 0
    absolute_freq = {}
    freq = {}
    for sent in conll:
        count += len(conll.sentence)
        for token in conll.sentence:
            absolute_freq[token.lemma] = absolute_freq.get(token.lemma,0)+1
    for k, v in absolute_freq.items():
        freq[k] = v/count

    return freq

