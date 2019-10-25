import re
import math

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize


def remove_special_chars(s):
    """ Remove all special characters from a given string

    :param s: String to be cleaned up
    :returns: String without special characters
    """
    stripped = re.sub('[^\w\s]', ' ', s)
    stripped = re.sub('_', ' ', stripped)

    # Make all whitespaces only one space
    stripped = re.sub('\s+', ' ', stripped)

    stripped = stripped.strip()

    return stripped


def count_words(sent):
    """ Count all the words of a given sentence

    :param sent: Sentence
    :returns: Amount of words in the sentence
    """
    words = word_tokenize(sent)
    return len(words)


def create_freq_dict(sents, lang):
    """ Create a frequency dict for each word 
        in each sentence

    :param sents: List of sentences
    :param lang: Language of the given text
    :returns: Dictionariy with the frequence of each word in each sentence
    """
    ix = 0
    freq_dict_all = []
    stop_words = set(stopwords.words(lang))

    for sent in sents:
        ix += 1
        freq_dict = {}
        words = word_tokenize(sent)

        for word in words:
            word = word.lower()
            if word not in stop_words:
                if word in freq_dict:
                    freq_dict[word] += 1
                else:
                    freq_dict[word] = 1

        temp = {
            'doc_id': ix,
            'freq_dict': freq_dict
        }

        freq_dict_all.append(temp)

    return freq_dict_all


def create_docs(text_sentences):
    """ Split the given text into sentences and count their words

    :param sent: Text to be splitted up
    :returns: Array of Dicts; Each contains an ID and the word count
    """
    doc_info = []

    ix = 0
    for sent in text_sentences:
        ix += 1
        count = count_words(sent)
        temp = {
                'doc_id': ix,
                'doc_length': count
        }
        doc_info.append(temp)

    return doc_info


def compute_tf(doc_info, freq_dict_all):
    """ Compute the TF-Score for all documents
        TF = (frequency of term in the doc / total terms in the doc)

    :param doc_info: Dict of Documents and their word count (from create_docs)
    :param freq_dict_all: Output of create_freq_dict
    :returns: Array of TF-Scores for all documents
    """
    tf_scores = []

    for temp_dict in freq_dict_all:
        id = temp_dict['doc_id']

        for k in temp_dict['freq_dict']:
            temp = {
                'doc_id': id,
                'TF_Score': temp_dict['freq_dict'][k] / doc_info[id - 1]['doc_length'],
                'key': k
            }

            tf_scores.append(temp)

    return tf_scores


def compute_idf(doc_info, freq_dict_all):
    """ Compute the IDF-Score for all documents

    :param doc_info: Dict of Documents and their word count (from create_docs)
    :param freq_dict_all: Output of create_freq_dict
    :returns: Array of IDF-Scores for all documents
    """
    idf_scores = []
    counter = 0

    for temp_dict in freq_dict_all:
        counter += 1

        for k in temp_dict['freq_dict'].keys():
            count = sum([k in tempdict['freq_dict'] for tempdict in freq_dict_all])
            temp = {
                'doc_id': counter,
                'IDF_Score': math.log(len(doc_info) / count),
                'key': k
            }

            idf_scores.append(temp)

    return idf_scores


def compute_tf_idf(tf_scores, idf_scores):
    """ Calculate the TF-IDF-Score for each document

    :param tf_scores: Output of compute_tf()
    :param idf_scores: Output of compute_idf()
    :returns: Dict with TF-IDF-Scores for each document
    """

    tfidf_scores = []

    for j in idf_scores:
        for i in tf_scores:
            if j['key'] == i['key'] and j['doc_id'] == i['doc_id']:
                temp = {
                    'doc_id': j['doc_id'],
                    'TFIDF_Score': j['IDF_Score'] * i['TF_Score'],
                    'key': i['key']
                }

                tfidf_scores.append(temp)

    return tfidf_scores


def get_sent_scores(tfidf_scores, text_sents, doc_info):
    """ Score all sentences based on the words TFIDF-Scores

    :param tfidf_scores: Matrix with the TFIDF-Scores for each word
    :param text_sents: All sentences as array
    :param doc_info: Dict of all doc_id's and their word count
    :returns: Score for each sentence
    """
    sent_info = []

    for doc in doc_info:
        sent_score = 0
        for i in range(0, len(tfidf_scores)):
            temp_dict = tfidf_scores[i]
            if doc['doc_id'] == temp_dict['doc_id']:
                sent_score += temp_dict['TFIDF_Score']

        temp = {
            'doc_id': doc['doc_id'],
            'sent_score': sent_score,
            'sentence': text_sents[doc['doc_id'] - 1]
        }
        sent_info.append(temp)

    return sent_info


def get_top_sents(sent_scores, top=None):
    """ Get the best sentences from all scores

    :param sent_scores: Dict with sentences and their scores
    :param top: Length to be returned, Returns all by default
    """
    sorted_sents = sorted(sent_scores, key=lambda k: k['sent_score'], reverse=True)

    if top:
        return sorted_sents[:top]
    else:
        return sorted_sents


def tfidf(text, amount, lang):
    """ Given a text, this returns a list of the best ranked sentences
        based on the TFIDF-Algorithm

    :param text: Text to be ranked
    :param amount: Amount of sentences returned, None means all sentences
    :param lang: Language of the given text
    :returns: Array of the best ranked sentences in the given text
    """
    # Preprocess the given text
    text_sents = sent_tokenize(text)
    text_sents_clean = [remove_special_chars(s) for s in text_sents]
    doc_info = create_docs(text_sents_clean)

    # Calculate the word frequence in each doc, the TF as well as the IDF-Score
    freq_dict = create_freq_dict(text_sents_clean, lang)
    tf_scores = compute_tf(doc_info, freq_dict)
    idf_scores = compute_idf(doc_info, freq_dict)

    # Calculate the TFIDF-Score based on the calculations above
    tfidf_scores = compute_tf_idf(tf_scores, idf_scores)

    # Score each individual sentence, sort and return them to the caller
    sent_scores = get_sent_scores(tfidf_scores, text_sents, doc_info)
    top_sents = get_top_sents(sent_scores=sent_scores, top=amount)

    return top_sents
