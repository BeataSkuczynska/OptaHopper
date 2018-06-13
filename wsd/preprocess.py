import codecs, os, re
from urllib.request import *

import lxml.etree as ET

out_path = 'out-szczerosci'
in_path = 'KorpusSzczerosci'

go = False

import json
import os
import time

url = "http://ws.clarin-pl.eu/nlprest2/base"


def upload(file):
    with open(file, "rb") as myfile:
        doc = myfile.read()
    return urlopen(Request(url + '/upload/', doc, {'Content-Type': 'binary/octet-stream'})).read()


def process(data):
    doc = json.dumps(data).encode("utf-8")
    taskid = urlopen(Request(url + '/startTask/', doc, {'Content-Type': 'application/json'})).read()
    time.sleep(0.2)
    resp = urlopen(Request(url + '/getStatus/' + taskid.decode('utf-8'))).read().decode("utf-8")
    data = json.loads(resp)
    while data["status"] == "QUEUE" or data["status"] == "PROCESSING":
        time.sleep(0.5)
        resp = urlopen(Request(url + '/getStatus/' + taskid.decode('utf-8'))).read().decode("utf-8")
        data = json.loads(resp)
    if data["status"] == "ERROR":
        print("Error " + data["value"])
        return None
    return data["value"]


for file in os.listdir(in_path):
    if file.endswith(".txt.tag"):
        if file in ['168_F.txt.tag']:
            print("skipping file")
            go = True
            continue
        if not go: continue
        doc = ET.parse(os.path.join(in_path, file))
        orthtags = {}

        # 1st pass to add indexing
        ix = 0
        for tokEl in doc.iter('tok'):
            orthEl = list(tokEl.iter('orth'))[0]
            ctagEl = list(tokEl.iter('ctag'))[0]
            orthtags[ix] = [orthEl.text, ctagEl.text]
            ix += 1
        ix = 0
        # 2nd pass to remove aglt and qub->aglt
        neworths = {}
        for ix, orthtag in orthtags.items():
            if ix > 0 and orthtag[1].find('aglt') >= 0:
                if ix > 1 and orthtags[ix - 1][1].find('qub') >= 0:
                    # print("QUB->AGLT:",  orthtags[ix-2], orthtags[ix-1],  orthtags[ix] )
                    orthtag[1] = orthtags[ix - 2][1]  # take tags of the N-2 token
                    orthtag[0] = orthtags[ix - 2][0] + orthtags[ix - 1][0] + orthtags[ix][0]  # concatenate orths
                    del neworths[ix - 2]
                    del neworths[ix - 1]
                    # print("changed to: "+orthtag[0])
                else:
                    # print( orthtags[ix-1],  orthtags[ix] )
                    orthtag[1] = orthtags[ix - 1][1]  # take tags of the former token
                    orthtag[0] = orthtags[ix - 1][0] + orthtags[ix][0]  # concatenate orths
                    del neworths[ix - 1]

            neworths[ix] = orthtag
            ix += 1

        txtfile = os.path.join(in_path, file[:-4])
        text = ' '.join(map(lambda x: x[0], neworths.values()))
        text = re.sub('\.([A-Z])', '. (1)', text)
        with codecs.open(txtfile, 'w', 'utf8') as fw:
            fw.write(text)

        print("Processing: " + txtfile)
        fileid = upload(txtfile)
        data = {'lpmn': lpmn, 'user': user, 'file': fileid.decode('utf-8')}
        data = process(data)
        if data is None: continue
        data = data[0]["fileID"]
        content = urlopen(Request(url + '/download' + data)).read()
        with open(os.path.join(out_path, file[:-8] + '.ccl'), "w") as outfile:
            outfile.write(content.decode('utf-8'))

        print("Processed fileid: " + str(fileid))

    # break
