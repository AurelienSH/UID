def read_conll(conll_fpath):
    conll_set = []
    with open(conll_fpath) as conll:
        l = conll.readline()
        sent_tmp = []
        text = ""
        while l:
            if l != "\n":
                if not l.startswith("#"):
                    if not "-" in l.split("\t")[0]:
                        sent_tmp.append(ConllToken(l))
                if l.startswith("# text"):
                    text = l.split("=")[1]
                if l.startswith("# sent_id"):
                    sent_id = l.split("=")[1]
            elif sent_tmp:
                conll_set.append(ConllSent(sent_tmp, text, sent_id))
                sent_tmp = []
            l = conll.readline()
    return conll_set
def get_genres(conll):
    genres = set()
    for sent in conll:
        genres.add(sent.genre)

    return genres

class ConllSent:
    def __init__(self, sent, text, sent_id):
        self.text = text
        self.sentence = sent
        self.cc_heads = self.get_cc_heads()
        self.genre = "_".join([sent_id.split("_")[1],sent_id.split("_")[2].split("-")[0]])

    def get_subj(self, gov_id):
        for token in self.sentence:
            if token.gov == gov_id and token.rel.startswith("subj"):
                subj = token
                return subj


    def get_group_size(self, gov_id, group_size=1):
        for token in self.sentence:
            if token.gov == gov_id:
                group_size += 1
                group_size += self.get_group_size(token.id, 0)
        return group_size

    def get_first_token_of_clause(self, head):
        first_tok_id = head.id
        for token in self.sentence:
            if token.gov == head.id:
                first_tok_id = min(self.get_first_token_of_clause(token), first_tok_id)
        return first_tok_id

    def get_cc_heads(self):
        cc_heads = []
        for token in self.sentence:
            gov = self[token.gov]
            if (token.upos == "VERB" or token.upos == "AUX") and (
                    (gov.lemma == "that") or (gov.upos == "VERB" and token.misc.get("VerbForm", False) == "Fin")) and not gov.rel == "udep":
                cc_heads.append(token)
        return cc_heads

    def __getitem__(self, index):
        return self.sentence[index - 1]


class ConllToken:
    def __init__(self, raw_token_line):
        id, form, lemma, upos, xpos, misc, gov, rel, _, _ = raw_token_line.split("\t")
        self.id = int(id.split(".")[0])
        self.form = form
        self.lemma = lemma
        self.upos = upos
        self.xpos = xpos
        if gov !="_":
            self.gov = int(gov.split(".")[0])
        else:
            self.gov = -1
        self.rel = rel
        self.misc = {k: v for k, v in [kv.split("=") for kv in misc.split("|") if len(kv.split("=")) == 2]}


if __name__ == "__main__":
    print("prout")
