import control_that
import utils.metrics as metrics
import utils.conll as conll
import csv


def get_data(sent, ud_sent):
    sentData = []
    count = 1
    for cc_head in sent.cc_heads:
        if cc_head.lemma != "can":
            m_verb = control_that.get_matrix_verb(ud_sent[cc_head.id], ud_sent)
            tmpdic = {
                'matrix_subject': control_that.get_matrix_subject(cc_head, sent),
                'frequency_matrix_verb': control_that.get_frequency_matrix_verb(cc_head, sent, freq),
                'word_form_similarity': control_that.get_word_sim(cc_head, sent),
                'frequency_CC_subject_head': control_that.get_frequency_cc_subject_head(cc_head, freq),
                'subject_form_CC_subject': control_that.get_CC_subject_availability(cc_head, sent),
                'position_matrix_verb': control_that.get_position_matrix_verb(cc_head, sent),
                'length_CC_remainder': control_that.get_length_cc_remainder(cc_head, sent),
                'length_CC_onset': control_that.get_length_cc_onset(cc_head, sent),
                'length_matrix_verb_to_CC': control_that.get_start_matrix_verb_to_cc(cc_head, sent),
                'that_omission': abs(control_that.get_that(cc_head, sent)-1),
                'uid': uid[m_verb.lemma],
                'genre': genres2id[sent.genre]
            }
            sentData.append(tmpdic)
            count += 1
    return sentData


if __name__ == "__main__":
    folder = '../Data/GUM/'
    full_conll = conll.read_conll(f"{folder}all_GUM.conllu")
    genres = conll.get_genres(full_conll)
    genres2id = {g:i for i, g in zip(range(len(genres)),genres)}
    id2genres = {i:g for g, i in genres2id.items()}
    cc_conll = conll.read_conll(f"{folder}CC_GUM/all_CC_SUD.conllu")
    ud_cc_conll = conll.read_conll(f"{folder}CC_GUM/all_CC_UD.conllu")
    freq, abs_freq = metrics.lemma_freq(full_conll)
    uid = metrics.uid_2010(full_conll)


    data = []
    for sud_sent, ud_sent in zip(cc_conll, ud_cc_conll):
        data += get_data(sud_sent, ud_sent)

    keys = data[0].keys()

    with open('../modeling/data.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
