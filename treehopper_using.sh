#!/usr/bin/env bash
#example input
###PARAMETERS
DIR=$1
MODEL_PATH=$2 #train or model path
LPMN=$3
USER=$4
FILENAME=$5

INPUT=${DIR}/${FILENAME}
# GET Sentences from conll format
mkdir resources/predict

if [[ ${INPUT} == *conll ]] ; then
    python3 scripts/prepare_conll_for_treehopper.py ${INPUT} resources/predict
    INPUT=resources/predict/sentences.txt
fi


#download treehopper
if [ ! -d trehopper ]; then
    echo " Downloading trehopper repository"
    git clone https://github.com/Zuchens/treehopper
fi
if [[ ${FILENAME} != *conll ]] ; then
    #get multiservice
    cd multiservice
    export PYTHONPATH=.
    sudo python2.7 -m pip install setuptools\=\=18.5.0
    sudo python2.7 -m pip install jsonpickle
    sudo python2.7 -m pip install thrift
    sudo easy_install-2.7 multiservice-0.1-py2.7.egg
    python2.7 thrift_client.py Concraft DependencyParser < ${INPUT} > ../resources/output_concraft.json
    cd ..

    #Multiservice to trehopper
    export PYTHONPATH=$(pwd)
    python3 scripts/multiservice_to_treehopper.py --input resources/output_concraft.json --output resources/predict
fi

#get wsd sentiments
mkdir resources/wsd_output
python3 wsd/raw_text.py --lpmn $LPMN --user $USER --out_path resources/wsd_output/input.ccl  --in_path ${DIR}
python3 emo/ascribe_sentiment_to_token.py --raw_text ${DIR} --wsd_output resources/wsd_output --wordnet resources/plwordnet-3.0.xml --out resources/predict


# get TreeLSTMSentiments
SENTIMENT_DICTIONARY=$(pwd)/resources/slownikWydzwieku01.csv
cd treehopper
./fetch_data.sh
sudo pip3 install -r requirements.txt
export PYTHONPATH=.

#TRAIN
if [ ${MODEL_PATH} = "train" ]; then
    python treehopper/train.py --dictionaries ${SENTIMENT_DICTIONARY}
    MODEL_PATH=models/saved_model/models/model.pth
fi
#PREDICT SENTIMENTS
MODEL_PATH=models/saved_model/models/model.pth
python treehopper/predict.py --model_path ${MODEL_PATH} \
               --input_parents ../resources/predict/parents.txt \
               --input_sentences ../resources/predict/sentences.txt \
               --input_wordnet ../resources/predict/input_wordnet.txt \
               --output ../resources/treehopper_sentiment.txt
cd ..

python add_treehopper_sentiment_to_conll.py resources/to_crf.conll resources/treehopper_sentiment.txt --output_path resources/

