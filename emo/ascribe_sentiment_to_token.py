import os
import re

import lxml.etree as ET

from tqdm import tqdm

wordnet_xml_file_path = '/home/komputerka/PycharmProjects/OptaHopper/resources/plwordnet_2_3/plwordnet_2_3.xml'
wsd_output = '/home/komputerka/PycharmProjects/OptaHopper/resources/output'

SENTIMENT_DICT = {'- m': "-2",
                  '- s': "-1",
                  '+ s': "1",
                  '+ m': "2"
                  }


def check_sentiment(desc):
    if "##A1" in desc:
        start_index = re.search('##A1', desc).span()[1] + 2
        sentiment_part = desc[start_index:]
        if sentiment_part:
            if sentiment_part[0] == "{":
                search_close_bracket = re.search('\} ', sentiment_part)
                if search_close_bracket:
                    sentiment_index_start = search_close_bracket.span()[1]
                    sentiment = sentiment_part[sentiment_index_start:sentiment_index_start+3]
                    if sentiment in SENTIMENT_DICT:
                        return SENTIMENT_DICT[sentiment]
                    else:
                        if sentiment_index_start < len(sentiment_part):
                            sentiment = sentiment_part[sentiment_index_start]
                            if sentiment == "0":
                                return "0"
            elif sentiment_part[0] == "0":
                return "0"
    return ""


def get_sentiment_dict():
    sentiment_dict = dict()
    doc = ET.parse(wordnet_xml_file_path)
    root = doc.getroot()
    for lexical_unit in tqdm(root):
        desc = lexical_unit.get('desc')
        if desc:
            sentiment = check_sentiment(desc)
            if sentiment:
                sentiment_dict[lexical_unit.get('id')] = sentiment
    return sentiment_dict


sentiment_dict = get_sentiment_dict()
for file in os.listdir(wsd_output):
    if file.endswith(".ccl"):
        sentiment_output = []
        doc = ET.parse(os.path.join(wsd_output, file))
        root = doc.getroot()
        for chunk in tqdm(root):
            for sentence in chunk:
                sentiment_sentence = []
                for token in sentence:
                    if token.tag == "tok":
                        has_synset_ascribed = False
                        for prop in token.iter('prop'):
                            if prop.get('key') == "sense:ukb:syns_id":
                                if prop.text in sentiment_dict:
                                    has_synset_ascribed = True
                                    sentiment_sentence.append(sentiment_dict[prop.text])
                                    break
                        if not has_synset_ascribed:
                            sentiment_sentence.append('0')
                sentiment_output.append(sentiment_sentence)
        with open(os.path.join(wsd_output, file[:-4] + "_sent"), 'w') as fo:
            for sentence in sentiment_output:
                fo.write(" ".join(sentence) + "\n")
