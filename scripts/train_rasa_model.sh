#!/bin/bash
cd ../rasa_nlu/
venv/bin/python -m rasa_nlu.train -c config_pinkpython_rasa.json
