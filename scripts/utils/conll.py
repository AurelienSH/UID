def read_conll(conll_fpath):
    conll_set = set()
    with open(conll_fpath) as conll:
        l = conll.readline()
        sent_tmp = []
        text = ""
        while l:
            if l != "\n":
                if not l.startswith("#"):
                    sent_tmp.append(ConllToken(l))
                if l.startswith("# text"):
                    text = l.split("=")[1]
            elif sent_tmp:
                conll_set.add(ConllSent(sent_tmp, text))
                sent_tmp = []
            l = conll.readline()
    return conll_set

class ConllSent:
    def __init__(self, sent, text):
        self.text = text
        self.sentence = sent

    def get_subj(self, gov_id):
        for token in self.sentence:
            if token.gov == gov_id and token.rel.startswith("subj"):
                subj = token
        return subj

    def get_group_size(self, gov_id, group_size = 1):
        for token in self.sentence:
            if token.gov == gov_id:
                group_size += 1
                group_size += self.get_group_size(token.id, 0)
        return group_size

    def get_first_token_of_clause(self,head):
        first_tok_id = head.id
        for token in self.sentence:
            if token.gov == head.id:
                first_tok_id = min(self.get_first_token_of_clause(token.id), self[first_tok_id])
        return self[first_tok_id]

    def __getitem__(self, index):
        return self.sentence[index-1]


class ConllToken:
    def __init__(self, raw_token_line):
        id, form, lemma, upos, xpos, _, gov, rel, _, _ = raw_token_line.split("\t")
        self.id = int(id)
        self.form = form
        self.lemma = lemma
        self.upos = upos
        self.xpos = xpos
        self.gov = gov
        self.rel = rel

if __name__ == "__main__":
    print("prout")