#!/usr/bin/env bash

if [ ! -d trehopper ]; then
    echo " Downloading trehopper repository"
    git clone https://github.com/Zuchens/treehopper
fi

cd treehopper
WITH_TRAIN=$1
SENTIMENT_DICTIONARY=SlownikWydzwieku01.csv

./fetch_data.sh
pip3 install -r requirements.txt
cd treehopper
export PYTHONPATH=$(pwd)

if [ ${WITH_TRAIN} == 'train']; then
    train.py --dictionaries ${SENTIMENT_DICTIONARY}
fi

python predict.py --model_path model.pth \
               --input_parents test/polevaltest_parents.txt \
               --input_sentences test/polevaltest_sentence.txt \
               --output ../../resources/treehopper_sentiment.txt

cd ../..
export PYTHONPATH=$(pwd)




python prepare_conll_for_treehopper.py resources/opta_test.conll resources/
python treehopper/treehopper/predict.py --model_path treehopper/model_1.pth --input_parents resources/parents.txt --input_sentences resources/sentences.txt --output resources/treehopper_sentiment.txt
python add_treehopper_sentiment_to_conll.py resources/opta_test.conll resources/treehopper_sentiment.txt --output_path resources/
