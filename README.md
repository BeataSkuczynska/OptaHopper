```
Running:  
./prepare_data INPUT MODEL_PATH LPMN USER   
for example  
./prepare_data "sample/input.txt" "train" LPMN USER   
INPUT=path to text file
MODEL_PATH="train" or TreeLSTM model path
LPMN=lpmn for WSD client
USER=user for WSD client
```

### Download OPFI & CRFSuite
- Opinion Finder - a hybrid (CRF+patterns) application for extracting opinion targets in Polish:
http://zil.ipipan.waw.pl/OPTA
by default the path is ./
- CRFSuite for Linux_64bit_binary
http://www.chokkan.org/software/crfsuite/
by default the path is opta-tagger/


#### Download Sentiment dictionary:
http://zil.ipipan.waw.pl/SlownikWydzwieku
by default the path is resources/slownikWydzwieku01.csv

### Install pytorch
for example
pip install http://download.pytorch.org/whl/cu80/torch-0.1.12.post2-cp35-cp35m-linux_x86_64.whl

### Download Wordnet
http://nlp.pwr.wroc.pl/plwordnet/download/?lang=pl
Default path : resources/plwordnet-3.0.xml
Take a version 3.0 or higher - otherwise it won't be compatible with WSD.

If something goes wrong check if you have the same directory structure as below  
```
OptaHopper
├── multiservice
│   ├── multiservice-0.1-py2.7.egg
│   └── thrift_client.py
├── opta-tagger
│   ├── add_sentiment.py
│   ├── crf-suite-0.12
│   │   ├── bin
│   │   ├── include
│   │   ├── lib
│   │   └── share
│   ├── crffeaturebuilder.py
│   ├── crfutils.py
│   ├── input_data
│   │   ├── conll-format
│   │   └── crf-format
│   ├── INSTALL
│   ├── models
│   ├── opta-patterns.py
│   ├── README
│   ├── resources
│   │   ├── pathsByIdWithMetadata.pkl
│   │   └── slownikWydzwieku01.csv
│   ├── runme.sh
│   ├── sentence.py
│   ├── SentencePatternMatcher.py
│   ├── train_data
│   ├── train_model.sh
│   │   ├── conll-format
│   │   │   └── train.conll
│   │   └── crf-format
│   │       └── train.crfsuite.txt
│   └── thrift_client.py
├── README.md
├── prepare_data.sh
├── requirements.txt
├── resources
│   ├── plwordnet-3.0.xml
│   └── slownikWydzwieku01.csv
├── sample
│   └── input.txt
├── scripts
│   ├── add_treehopper_sentiment_to_conll.py
│   ├── __init__.py
│   ├── multiservice_to_treehopper.py
│   ├── prepare_conll_for_treehopper.py
│   └── utils.py
├── treehopper
│   ├── fetch_data.sh
│   ├── finals
│   ├── LICENSE
│   ├── models
│   │   └── saved_model
│   │       └── models
│   │           ├── config.txt
│   │           └── model.pth
│   ├── README.md
│   ├── requirements.txt
│   ├── data
│   │   └── pol
│   │       └── fasttext
│   │           ├── wiki.pl.bin
│   │           └── wiki.pl.vec
│   ├── results
│   ├── test
│   │   ├── polevaltest_labels.txt
│   │   ├── polevaltest_parents.txt
│   │   ├── polevaltest_rels.txt
│   │   ├── polevaltest_sentence.txt
│   │   └── polevaltest_wordnet.txt
│   ├── tmp
│   │   ├── new_words.txt
│   │   └── vocab.txt
│   ├── training-treebank
│   │   ├── README
│   │   ├── rev_labels.txt
│   │   ├── rev_parents.txt
│   │   ├── rev_rels.txt
│   │   ├── rev_sentence.txt
│   │   ├── rev_wordnet.txt
│   │   ├── sklad_labels.txt
│   │   ├── sklad_parents.txt
│   │   ├── sklad_rels.txt
│   │   ├── sklad_sentence.txt
│   │   └── sklad_wordnet.txt
│   ├── treehopper
│   │   ├── config.py
│   │   ├── data
│   │   │   ├── constants.py
│   │   │   ├── dataset.py
│   │   │   ├── embeddings.py
│   │   │   ├── __init__.py
│   │   │   ├── split_datasets.py
│   │   │   └── vocab.py
│   │   ├── evaluate.py
│   │   ├── feature_selection
│   │   │   ├── gridsearch.py
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   ├── input.ccl
│   │   ├── model
│   │   │   ├── __init__.py
│   │   │   ├── model.py
│   │   │   ├── sentiment_trainer.py
│   │   │   ├── training.py
│   │   │   ├── tree.py
│   │   │   └── zoneout.py
│   │   ├── predict.py
│   │   ├── tmp
│   │   └── train.py
│   └── wiki.pl.zip
└── wsd_emo
    ├── ascribe_sentiment_to_token.py
    └── raw_text.py
   ```
