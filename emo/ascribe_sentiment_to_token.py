import argparse
import os
import re

import lxml.etree as ET
from tqdm import tqdm

SENTIMENT_DICT = {'- m': "-2",
                  '- s': "-1",
                  '+ s': "1",
                  '+ m': "2"
                  }


def check_if_neutral_sentiment(sentiment_part, sentiment_index_start):
    if sentiment_index_start < len(sentiment_part):
        sentiment = sentiment_part[sentiment_index_start]
        if sentiment == "0":
            return "0"
    return ""


def retrieve_sentiment_from_sentiment_annotation(sentiment_part):
    if sentiment_part[0] == "{":
        search_close_bracket = re.search('\} ', sentiment_part)
        if search_close_bracket:
            sentiment_index_start = search_close_bracket.span()[1]
            sentiment = sentiment_part[sentiment_index_start:sentiment_index_start + 3]
            if sentiment in SENTIMENT_DICT:
                return SENTIMENT_DICT[sentiment]
            else:
                return check_if_neutral_sentiment(sentiment_part, sentiment_index_start)
    elif sentiment_part[0] == "0":
        return "0"
    return ""


def retrieve_sentiment_from_lu_description(desc):
    if "##A1" in desc:
        start_index = re.search('##A1', desc).span()[1] + 2
        sentiment_part = desc[start_index:]
        if sentiment_part:
            return retrieve_sentiment_from_sentiment_annotation(sentiment_part)
    return ""


def get_sentiment_dict(args):
    sentiment_dict = dict()
    doc = ET.parse(args.wordnet)
    root = doc.getroot()
    for lexical_unit in tqdm(root):
        desc = lexical_unit.get('desc')
        if desc:
            sentiment = retrieve_sentiment_from_lu_description(desc)
            if sentiment:
                sentiment_dict[lexical_unit.get('id')] = sentiment
    return sentiment_dict


def ascribe_sentiment(token, sentiment_sentence, emo_sentiment_dict):
    has_synset_ascribed = False
    for prop in token.iter('prop'):
        if prop.get('key') == "sense:ukb:syns_id" and prop.text in emo_sentiment_dict:
            has_synset_ascribed = True
            sentiment_sentence.append(emo_sentiment_dict[prop.text])
            break
    if not has_synset_ascribed:
        sentiment_sentence.append('0')
    return sentiment_sentence


def get_token_orth(token):
    current_orth = ""
    for orth in token.iter('orth'):
        current_orth = orth.text
        if "&" in current_orth:
            current_orth = "&"
        break
    return current_orth


def get_sentiment_for_tokens(sentence, emo_sentiment_dict, raw_text, previous_raw_token):
    sentiment_sentence = []
    current_raw_token = ""
    for token in sentence:
        if token.tag == "tok":
            current_orth = get_token_orth(token)
            if not current_raw_token:
                current_raw_token = raw_text.pop(0)
            if current_orth in current_raw_token:
                sentiment_sentence = ascribe_sentiment(token, sentiment_sentence, emo_sentiment_dict)
                previous_raw_token = current_raw_token
                current_raw_token = ""
            elif current_orth in previous_raw_token:
                if sentiment_sentence and sentiment_sentence[-1] == "0":
                    sentiment_sentence = ascribe_sentiment(token, sentiment_sentence[:-1], emo_sentiment_dict)
                elif not sentiment_sentence:
                    sentiment_sentence = ascribe_sentiment(token, sentiment_sentence, emo_sentiment_dict)
    return sentiment_sentence, raw_text, previous_raw_token


def save_ascribed_sentiment(path, filename, sentiment_output, sentences_sizes):
    with open(os.path.join(path, filename[:-4] + "_wordnet.txt"), 'w') as fo:
        for sentence_size in sentences_sizes:
            fo.write(" ".join(sentiment_output[:sentence_size]) + "\n")
            sentiment_output = sentiment_output[sentence_size:]


def load_raw(raw_text_directory, filename):
    raw_text = []
    sentences_sizes = []
    with open(os.path.join(raw_text_directory, filename + ".txt"), "r") as raw:
        lines = raw.readlines()
        for line in lines:
            line_s = line.strip().split(" ")
            raw_text.extend(line_s)
            sentences_sizes.append(len(line_s))
    return raw_text, sentences_sizes


def main(args):
    emo_sentiment_dict = get_sentiment_dict(args)
    for file in os.listdir(args.wsd_output):
        if file.endswith(".ccl"):
            raw_text, sentences_sizes = load_raw(args.raw_text, file[:-4])
            sentiment_output = []
            previous_raw_token = ""
            doc = ET.parse(os.path.join(args.wsd_output, file))
            root = doc.getroot()
            for chunk in tqdm(root):
                for sentence in chunk:
                    if sentence.tag == "sentence":
                        sentiment_sentence, raw_text, previous_raw_token = \
                            get_sentiment_for_tokens(sentence, emo_sentiment_dict, raw_text, previous_raw_token)
                        sentiment_output.extend(sentiment_sentence)
            save_ascribed_sentiment(args.output, file, sentiment_output, sentences_sizes)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PyTorch TreeLSTM for Sentiment Analysis Trees')
    parser.add_argument('--raw_text')
    parser.add_argument('--wsd_output')
    parser.add_argument('--output')
    parser.add_argument('--wordnet')
    args = parser.parse_args()
    main(args)
