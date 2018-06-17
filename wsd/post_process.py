import codecs, os, re, copy
import xml.etree.ElementTree
import lxml.etree
import pandas as pd

szcz_path = 'out-szczerosci'
utf8_html_parser = lxml.etree.HTMLParser(encoding='utf-8')

rowlist = []

filenr = 0
qubagltmod = 0
agltmod = 0

for file in os.listdir(szcz_path):
    if file.endswith(".ccl"):
        print(file)
        e = xml.etree.ElementTree.parse(szcz_path + '/' + file, parser=utf8_html_parser).getroot()
        orthtags = {}
        ix = 0
        for tokEl in e.findall(".//tok"):
            # surprisingly next 4 lines have to be exactly like this:
            orthEl = list(tokEl.iter('orth'))[0]
            ctagEl = list(tokEl.iter('ctag'))[0]
            lexEl = tokEl.find('lex')
            baseEl = lexEl.find('base')

            propsList = list(tokEl.iter('prop'))
            chosenSynset = None
            lcm_tag = None
            if len(propsList) > 0:
                propEl = propsList[0]
                key = propEl.get('key')
                if key is not None and key == 'sense:ukb:syns_id':
                    if propEl.text is not None: # and not lcm_added:
                        chosenSynset = float(propEl.text.strip())
                        # Paulina to Cie interesuje -> chosenSynset

                        # if str(chosenSynset) + "_" + baseEl.tail in lcm_senses:
                        #     lcm_tag = lcm_senses[str(chosenSynset) + "_" + baseEl.tail]
                else:
                    print("picked wrong prop!")
            orthtags[ix] = [orthEl.text, ctagEl.text, baseEl.tail, chosenSynset, lcm_tag, file]
            ix += 1

        # 2nd pass to remove aglt and qub->aglt
        neworths = {}
        ix = 0
        for ix, orthtag in orthtags.items():
            if ix > 0 and orthtag[1].find('aglt') >= 0:
                if ix > 1 and orthtags[ix - 1][1].find('qub') >= 0:
                    # print("QUB->AGLT:",  orthtags[ix-2], orthtags[ix-1],  orthtags[ix] )
                    orthtag[1:] = orthtags[ix - 2][1:]  # take tags, synset and LCM of the N-2 token
                    orthtag[0] = orthtags[ix - 2][0] + orthtags[ix - 1][0] + orthtags[ix][0]  # concatenate orths
                    del neworths[ix - 2]
                    del neworths[ix - 1]
                    # print("changed to: "+orthtag[0])
                    qubagltmod += 1
                else:
                    # print( orthtags[ix-1],  orthtags[ix] )
                    orthtag[1:] = orthtags[ix - 1][1:]  # take tags, synset and LCM of the former token
                    orthtag[0] = orthtags[ix - 1][0] + orthtags[ix][0]  # concatenate orths
                    del neworths[ix - 1]
                    # print("changed to: "+orthtag[0])
                    agltmod += 1

            neworths[ix] = orthtag
            # print(neworths[ix])
            row = copy.deepcopy(orthtag)
            row.insert(0, ix)
            rowlist.append(row)
            ix += 1

        filenr += 1
        print(filenr)
        # break


df = pd.DataFrame(rowlist, columns=['ix', 'orth', 'ctags', 'base', 'synset', 'lcm', 'file'])
writer = df.to_csv('szczerosc-lcm.csv')
print ("qubagltmod: " + str(qubagltmod) + " agltmod:" + str(agltmod))