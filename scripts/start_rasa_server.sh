#!/bin/bash
cd ../rasa_nlu/
venv/bin/python -m rasa_nlu.server -c config_pinkpython_rasa.json -d=./$1/ -e api &
