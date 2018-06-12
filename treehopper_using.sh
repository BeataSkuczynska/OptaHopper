#!/usr/bin/env bash
if [ ! -d trehopper ]; then
    echo " Downloading trehopper repository"
    git clone https://github.com/Zuchens/treehopper
fi
if [ ! -d OPTA ]; then
    echo " Downloading OPTA"
 #   wget http://zil.ipipan.waw.pl/OPTA?action=AttachFile&do=get&target=opta-tagger.tar.gz
#    tar -xzf OPTA-patterns-0.1.tar.gz
fi
if [ ! -d out-szczerosci ]; then
    mkdir out-szczerosci
fi
# download Korpus Szczerosci

python prepare_conll_for_treehopper.py resources/opta_test.conll resources/
python treehopper/treehopper/predict.py --model_path treehopper/model_1.pth --input_parents resources/parents.txt --input_sentences resources/sentences.txt --output resources/treehopper_sentiment.txt
python add_treehopper_sentiment_to_conll.py resources/opta_test.conll resources/treehopper_sentiment.txt --output_path resources/
