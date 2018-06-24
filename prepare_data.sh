#!/usr/bin/env bash
###PARAMETERS
INPUT=$1
MODEL_PATH=$2 #train or model path
LPMN=$3
USER=$4


sudo python3 -m pip install -r requirements.txt

if [ ! -d resources ]; then
    mkdir resources resources/predict
fi


if [ ! -d treehopper ]; then
    echo " Downloading trehopper repository"
    git clone https://github.com/Zuchens/treehopper
fi

echo "Parse sentence in multiservice"
cd multiservice
export PYTHONPATH=.
sudo python2.7 -m pip install setuptools\=\=18.5.0
sudo python2.7 -m pip install jsonpickle
sudo python2.7 -m pip install thrift
sudo easy_install-2.7 multiservice-0.1-py2.7.egg
python2.7 thrift_client.py Concraft DependencyParser < ../${INPUT} > ../resources/output_concraft.json
cd ..

echo "Multiservice to trehopper"
export PYTHONPATH=$(pwd)
python scripts/multiservice_to_treehopper.py --input resources/output_concraft.json --output resources/predict


echo "get wsd_emo sentiments"
python wsd_emo/raw_text.py --lpmn $LPMN --user $USER --out_path resources/wsd_output.txt  --in_path ${INPUT}
python wsd_emo/ascribe_sentiment_to_token.py --raw_text resources/predict/sentences.txt --wsd_output resources/wsd_output.txt --wordnet resources/plwordnet-3.0.xml --out resources/predict


echo "get TreeLSTM Sentiments"
SENTIMENT_DICTIONARY=$(pwd)/resources/slownikWydzwieku01.csv
cd treehopper
./fetch_data.sh
sudo pip3 install -r requirements.txt
export PYTHONPATH=.

if [ ${MODEL_PATH} = "train" ]; then
    echo "train TreeLSTM"
    python treehopper/train.py --dictionaries ${SENTIMENT_DICTIONARY}
    MODEL_PATH=models/saved_model/models/model.pth
fi
echo "PREDICT SENTIMENTS"
python treehopper/predict.py --model_path ${MODEL_PATH} \
               --input_parents ../resources/predict/parents.txt \
               --input_sentences ../resources/predict/sentences.txt \
               --input_wordnet ../resources/predict/sentiment_wordnet.txt \
               --output ../resources/treehopper_sentiment.txt
cd ..

export PYTHONPATH=$(pwd)
echo "Prepare treehopper sentiment for OPFI"
python scripts/add_treehopper_sentiment_to_conll.py resources/predict/to_crf.conll resources/treehopper_sentiment.txt --output_path resources/


sudo python2.7 -m pip install pyparsing
cd opta-tagger
if [ ! -d input_data ]; then
    mkdir input_data input_data/conll-format input_data/crf-format
fi
export PYTHONPATH=.
echo "Train CRF with default OPFI dataset"
cat train_data/conll-format/train.conll | python2.7 crffeaturebuilder.py > train_data/crf-format/train.crfsuite.txt
crfsuite-0.12/bin/crfsuite learn -m models/opta.model train_data/crf-format/train.crfsuite.txt

echo "Get file with opinion target for every token"
python2.7 opta_patterns.py ../resources/with_treehopper_sentiment.conll input_data/conll-format/target.conll
cat input_data/conll-format/target.conll | python2.7 crffeaturebuilder.py > input_data/crf-format/target.txt
crfsuite-0.12/bin/crfsuite tag -m models/opta.model input_data/crf-format/target.txt > ../resources/predict/target.conll