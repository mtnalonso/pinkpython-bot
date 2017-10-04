#!/bin/bash

set -Ee

ROOT_DIR=$(cd $(dirname $0) && pwd -L)

VENV_DIR="${ROOT_DIR}/.venv"

if [ ! -d ${VENV_DIR} ]; then
    virtualenv -p python3 ${VENV_DIR}
fi

source ${VENV_DIR}/bin/activate

function install_rasa {
  # ====== RASA Installation ======
  git clone https://github.com/RasaHQ/rasa_nlu.git
  cd rasa_nlu

  # TODO: checkout OS and distribution
  sudo apt-get install -y libblas-dev liblapack-dev

  pip install -r requirements.txt
  python setup.py install
  pip install spacy
  python -m spacy download en

  pip install scipy
  pip install scikit-learn
  pip install sklearn-crfsuite

  cd ${ROOT_DIR}

  cp scripts/config_pinkpython_rasa.json rasa_nlu/
  cp -r npl_models/pinkpython-bot/ rasa_nlu/data/
}

os=`uname`

if [ "$os" == "Linux" ]; then
  install_rasa
else
  echo "Only linux is supported for 'rasa' installation"
fi
