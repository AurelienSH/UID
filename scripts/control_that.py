from utils import conll

def get_start_matrix_verb_to_cc(cc_head, sent):
    return (cc_head.gov-sent.get_first_token_of_clause(cc_head).id)-1

def get_length_cc_onset(cc_head, sent):
    subj = sent.get_subj(cc_head.id)
    return sent.get_group_size(subj.id)

def get_length_cc_remainder(cc_head, sent):
    subj = sent.get_subj(cc_head.id)
    return sent.get_group_size(cc_head)-sent.get_group_size(subj)

def get_position_matrix_verb():
    return

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
    if subj.upos == "PRON":
        if subj.lemma == "I":
            return 1
        elif subj.lemma == "it":
            return 2
        return 3
    return 4

def get_subject_identity(cc_head):
    return

def get_frequency_cc_subject_head(cc_head):
    return

def get_word_sim(cc_head, sent):
    return

def get_frequency_matrix_subject(cc_head):
    return

def get_ambiguous_cc_onset():
    return

def get_matrix_subject():
    return

def get_syntactic_persistence():
    return

def get_speaker_gender():
    return

def get_speaker_gender():
    return