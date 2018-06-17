import codecs, os, re
from urllib.request import *


out_path = '/home/komputerka/PycharmProjects/OptaHopper/resources/output'
in_path = '/home/komputerka/PycharmProjects/OptaHopper/resources/input'

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
    txtfile = os.path.join(in_path, file)
    with codecs.open(txtfile, 'r', 'utf8') as fw:
        text = fw.read()

    print("Processing: " + txtfile)
    fileid = upload(txtfile)
    data = {'lpmn': lpmn, 'user': user, 'file': fileid.decode('utf-8')}
    data = process(data)
    if data is None:
        continue
    data = data[0]["fileID"]
    content = urlopen(Request(url + '/download' + data)).read()
    with open(os.path.join(out_path, file[:-4] + '.ccl'), "w") as outfile:
        outfile.write(content.decode('utf-8'))

    print("Processed fileid: " + str(fileid))


