import argparse
import os

from utils import get_conll


def save_treehopper_input_files(conll, output_path):
    if output_path:
        sentences_fname = os.path.join(output_path, "sentences.txt")
        parents_fname = os.path.join(output_path, "parents.txt")
    else:
        sentences_fname = "sentences.txt"
        parents_fname = "parents.txt"
    with open(sentences_fname, 'w') as sentences_file, open(parents_fname, 'w') as parents_file:
        for sentence in conll:
            words_to_write = []
            parents_id_to_write = []
            for token in sentence:
                splitted_token = token.strip().split(" ")
                word = splitted_token[1]
                parent_id = splitted_token[6]
                words_to_write.append(word)
                parents_id_to_write.append(parent_id)
            sentences_file.write(" ".join(words_to_write) + "\n")
            parents_file.write(" ".join(parents_id_to_write) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create two files needed fo use treehopper for sentiment prediction')
    parser.add_argument('input_path', help='Path to CONLL file', type=str)
    parser.add_argument('output_path', help='Path to save treehopper files', type=str)
    args = parser.parse_args()

    conll = get_conll(args.input_path)
    save_treehopper_input_files(conll, args.output_path)
