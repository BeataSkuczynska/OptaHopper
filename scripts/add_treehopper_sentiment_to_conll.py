import argparse
import os
from itertools import zip_longest

from scripts.utils import get_conll


def add_sentiment_to_conll(conll, sentiments, output_path):
    conll_output_fname = os.path.join(output_path, "with_treehopper_sentiment.conll") if output_path else "with_treehopper_sentiment.conll"
    with open(conll_output_fname, "w") as output:
        for c_sentence, s_sentence in zip(conll, sentiments):
            for token, sentiment in zip_longest(c_sentence, s_sentence):
                try:
                    token_splitted = token.strip().split("\t")[:8]
                except AttributeError:
                    print(token)
                if sentiment in ["-1",  "1"]:
                    token_splitted.extend("_"*3 + "S")
                else:
                    token_splitted.extend("_" * 4)
                output.write("\t".join(token_splitted) + "\n")
            output.write("\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Adds sentiment column to conll file')
    parser.add_argument('conll_path', help='Path to CONLL file', type=str)
    parser.add_argument('sentiment_path', help='Path to file with tree sentiment from treehopper', type=str)
    parser.add_argument('--output_path', help='Path to save treehopper files', type=str, required=False)
    args = parser.parse_args()

    conll = get_conll(args.conll_path)
    with open(args.sentiment_path) as f:
        sentiments = list(f.readlines())
    sentiments = [sentence.strip().split(" ") for sentence in sentiments]
    add_sentiment_to_conll(conll, sentiments, args.output_path)
