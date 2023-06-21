from utils import conll2, metrics
import numpy as np

def get_matrix_verb(cc_head, sent):
    dep = sent.ud[cc_head.id-1]
    return sent[dep.gov]

def find_verb(token, sent):
    if token.upos != "VERB" and token.upos != "AUX":
        return find_verb(sent[token.id-1], sent)
    return token

def get_that(cc_head, sent):
    marks = sent.get_deps(cc_head, "mark")
    for mark in marks:
        if mark.form == "that":
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
                return 0
            elif subj.lemma == "it":
                return 1
            return 2
    return 3

def get_subject_identity(cc_head):
    return

def get_frequency_cc_subject_head(cc_head, freq, sent):
    return np.log(freq.get(metrics.get_lemma(cc_head, sent), 0))

def get_word_sim(cc_head, sent):
    if sent[sent.get_first_token_of_clause(cc_head)].lemma == 'that':
        return 1
    return 0

def get_frequency_matrix_verb(cc_head, sent, freq):
    m_verb = get_matrix_verb(cc_head, sent)
    return np.log(freq.get(metrics.get_lemma(m_verb, sent), 0))

def get_ambiguous_cc_onset():
    return

def get_matrix_subject(cc_head, sent):
    m_verb = get_matrix_verb(cc_head, sent)
    subj = sent.get_subj(m_verb.id)
    if subj:
        if subj.upos == "PRON":
            if subj.lemma == "I":
                return 0
            elif subj.lemma == "you":
                return 1
            return 2
    return 3

def get_syntactic_persistence():
    return

def get_speaker_gender():
    return