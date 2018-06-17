import json
import os

path = '/home/komputerka/PycharmProjects/OptaHopper/resources/'

with open(os.path.join(path + "output_concraft.json")) as js:
    parsed_sents = json.load(js)

with open(os.path.join(path, "sentences"), "w") as sents, open(os.path.join(path, "parents"), "w") as parents, \
        open(os.path.join(path, "rels"), "w") as rels, open(os.path.join(path, "to_crf.conll"), "w") as conll:
    for paragraph in parsed_sents['paragraphs']:
        for sentence in paragraph['sentences']:
            parents_s, rels_s, sent, conll_s = [], [], [], []
            id = 0
            for token_depparse in sentence['dependencyParse']:
                conll_t = []
                id += 1
                conll_t.append(str(id))
                parent = token_depparse["startTokenId"]
                if parent:
                    parent_id = str(int(parent[-1])+1)
                    parents_s.append(parent_id)
                    conll_t.append(parent_id)
                else:
                    parents_s.append("0")
                    conll_t.append("0")
                label = token_depparse["label"]
                rels_s.append(label)
                conll_t.append(label)
                conll_s.append(conll_t)
            parents.write(" ".join(parents_s) + "\n")
            rels.write(" ".join(rels_s) + "\n")
            for token, conll_t in zip(sentence['tokens'], conll_s):
                orth = token['orth']
                sent.append(orth)
                conll_t.insert(1, orth)
                interp = token["chosenInterpretation"]
                conll_t.insert(2, interp['base'])
                conll_t.insert(3, interp['ctag'])
                conll_t.insert(4, interp['ctag'])
                conll_t.insert(5, interp['msd'])
                conll_t.extend(["_"]*3)
            sents.write(" ".join(sent) + "\n")
            for conll_t in conll_s:
                conll.write("\t".join(conll_t) + "\n")
            conll.write("\n")
