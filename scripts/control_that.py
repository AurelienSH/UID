from utils import conll
import numpy as np

def get_matrix_verb(cc_head, sent):
    if sent[cc_head.gov].lemma == "that" :
        return get_matrix_verb(sent[cc_head.gov], sent)
    if sent[cc_head.gov].upos != "VERB" and sent[cc_head.gov].upos != "AUX":
        return find_verb(sent[cc_head.gov], sent)
    return sent[cc_head.gov]
def find_verb(token, sent):
    if token.upos != "VERB" and token.upos != "AUX":
        return find_verb(sent[token.id-1], sent)
    return token
def get_that(cc_head, sent):
    if sent[cc_head.gov].form == "that":
        return 1
    return 0

def get_start_matrix_verb_to_cc(cc_head, sent):
    if get_that(cc_head, sent):
        return (sent[cc_head.gov].gov - sent[sent.get_first_token_of_clause(cc_head)].id) - 1
    return cc_head.gov-sent[sent.get_first_token_of_clause(cc_head)].id

def get_length_cc_onset(cc_head, sent):
    subj = sent.get_subj(cc_head.id)
    if subj:
        return sent.get_group_size(subj.id)
    return 0

def get_length_cc_remainder(cc_head, sent):
    subj = sent.get_subj(cc_head.id)
    return sent.get_group_size(cc_head)-sent.get_group_size(subj)

def get_position_matrix_verb(cc_head, sent):
    return get_matrix_verb(cc_head, sent).id-1

def get_log_speech_rate():
    return

def get_squared_log_speech_rate():
    return

def get_pause():
    return

def get_disfluency():
    return

def get_CC_subject_availability(cc_head, sent):
    subj = sent.get_subj(cc_head.id)
    if subj:
        if subj.upos == "PRON":
            if subj.lemma == "I":
                return 1
            elif subj.lemma == "it":
                return 2
            return 3
    return 4

def get_subject_identity(cc_head):
    return

def get_frequency_cc_subject_head(cc_head, freq):
    return np.log(freq[cc_head.lemma])

def get_word_sim(cc_head, sent):
    if sent[sent.get_first_token_of_clause(cc_head)].lemma == 'that':
        return 1
    return 0

def get_frequency_matrix_verb(cc_head, sent, freq):
    m_verb = get_matrix_verb(cc_head, sent)
    return np.log(freq[m_verb.lemma])

def get_ambiguous_cc_onset():
    return

def get_matrix_subject(cc_head, sent):
    m_verb = get_matrix_verb(cc_head, sent)
    subj = sent.get_subj(m_verb.id)
    if subj:
        if subj.upos == "PRON":
            if subj.lemma == "I":
                return 1
            elif subj.lemma == "you":
                return 2
            return 3
    return 4

def get_syntactic_persistence():
    return

def get_speaker_gender():
    return