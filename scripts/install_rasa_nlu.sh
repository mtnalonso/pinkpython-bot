#!/bin/bash

cd ..
git clone https://github.com/RasaHQ/rasa_nlu.git
cd rasa_nlu
virtualenv venv
source venv/bin/activate
sudo apt-get install -y libblas-dev liblapack-dev
pip install -r requirements.txt
pip install spacy
python -m spacy download en
pip install scipy
pip install scikit-learn
pip install sklearn-crfsuite

cp scripts/config_pinkpython_rasa.json rasa_nlu/
cp -r nlp_models/pinkpython-bot/ rasa_nlu/data/
