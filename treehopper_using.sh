#!/usr/bin/env bash

python prepare_conll_for_treehopper.py resources/opta_test.conll resources/
python treehopper/treehopper/predict.py --model_path treehopper/model_1.pth --input_parents resources/parents.txt --input_sentences resources/sentences.txt --output resources/treehopper_sentiment.txt
python add_treehopper_sentiment_to_conll.py resources/opta_test.conll resources/treehopper_sentiment.txt --output_path resources/
