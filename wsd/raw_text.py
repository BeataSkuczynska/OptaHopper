import argparse
import json
import os
import time
from urllib.request import *

url = "http://ws.clarin-pl.eu/nlprest2/base"


def upload(file):
    with open(file, "rb") as myfile:
        doc = myfile.read()
    return urlopen(Request(url + '/upload/', doc, {'Content-Type': 'binary/octet-stream'})).read()


def process(data):
    doc = json.dumps(data).encode("utf-8")
    print(doc)
    taskid = urlopen(Request(url + '/startTask/', doc, {'Content-Type': 'application/json'})).read()
    time.sleep(0.2)
    resp = urlopen(Request(url + '/getStatus/' + taskid.decode('utf-8'))).read().decode("utf-8")
    print(resp)
    data = json.loads(resp)
    while data["status"] == "QUEUE" or data["status"] == "PROCESSING":
        time.sleep(0.5)
        resp = urlopen(Request(url + '/getStatus/' + taskid.decode('utf-8'))).read().decode("utf-8")
        data = json.loads(resp)
    if data["status"] == "ERROR":
        print("Error " + data["value"])
        return None
    return data["value"]


def main(args):
    for file in os.listdir(args.in_path):
        txtfile = os.path.join(args.in_path, file)
        print("Processing: " + txtfile)
        fileid = upload(txtfile)
        data = {'lpmn': args.lpmn, 'user': args.user, 'file': fileid.decode('utf-8')}
        data = process(data)
        if data is None:
            continue
        data = data[0]["fileID"]
        content = urlopen(Request(url + '/download' + data)).read()

        out_filename = file[:-4] + '.ccl'
        with open(os.path.join(args.out_path, out_filename), "w") as outfile:
            outfile.write(content.decode('utf-8'))

        print("Processed fileid: " + str(fileid))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PyTorch TreeLSTM for Sentiment Analysis Trees')
    parser.add_argument('--lpmn')
    parser.add_argument('--user')
    parser.add_argument('--out_path')
    parser.add_argument('--in_path')

    args = parser.parse_args()
    main(args)

