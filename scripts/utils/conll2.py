import numpy as np

def read_conll(conll_fpath, udfpath):
    conll_set = []
    with open(udfpath) as u:
        with open(conll_fpath) as conll:
            l = conll.readline()
            lud = u.readline()
            sent_tmp = []
            udsent = []
            text = ""
            while l and lud:
                if l != "\n" and lud != "\n":
                    if not l.startswith("#") and not lud.startswith("#"):
                        if not "-" in l.split("\t")[0] and not "-" in lud.split("\t")[0]:
                            if l.split("\t")[0] != lud.split("\t")[0]:
                                print(l.split("\t")[1])
                                print(lud.split("\t")[1])
                                print(prout)
                            sent_tmp.append(ConllToken(l))
                            udsent.append(ConllToken(lud))
                    if l.startswith("# text"):
                        text = l.split("=")[1]
                    if l.startswith("# sent_id"):
                        sent_id = l.split("=")[1]

                elif sent_tmp:
                    conll_set.append(ConllSent(sent_tmp, udsent, text, sent_id))
                    sent_tmp = []
                    udsent = []
                l = conll.readline()
                lud = u.readline()
    return conll_set


def get_genres(conll):
    genres = set()
    for sent in conll:
        genres.add(sent.genre)

    return genres

class ConllSent:
    def __init__(self, sent, udsent, text, sent_id):
        self.text = text
        self.sentence = sent
        self.ud = udsent
        self.cc_heads = self.get_cc_heads()
        self.genre = np.random.randint(0,2)
        self.id = sent_id

    def get_subj(self, gov_id):
        for token in self.sentence:
            if token.gov == gov_id and token.rel.startswith("subj"):
                subj = token
                return subj

    def get_deps(self, gov, rel):
        objs = []
        for tok in self.ud:
            if tok.gov == gov.id and tok.rel == rel:
                objs.append(tok)
        return objs

    def get_depsSud(self, gov, rel):
        objs = []
        for tok in self.sentence:
            if tok.gov == gov.id and tok.rel == rel:
                objs.append(tok)
        return objs

    def get_form(self, form):
        toks = []
        for tok in self.ud:
            if tok.form == form:
                toks.append(tok)
        return toks

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
        for i, token in enumerate(self.ud):
            if token.rel == "ccomp":
                objs = self.get_deps(token, "obj")
                subj = self.get_deps(token, "nsubj")
                whats = self.get_form("what")
                check = True
                if subj:
                    if subj[0].form == "what":
                        check = False
                for obj in objs:
                    for what in whats:
                        if what.rel == "det" and what.gov == obj.id:
                            check = False

                if check:
                    cc_heads.append(self.sentence[i])
        return cc_heads

    def __getitem__(self, index):
        return self.sentence[index - 1]


class ConllToken:
    def __init__(self, raw_token_line):
        id, form, lemma, upos, xpos, misc, gov, rel, _, _ = raw_token_line.split("\t")
        if not "-" in id:
            self.id = int(id.split(".")[0])
        else:
            self.id = id
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
