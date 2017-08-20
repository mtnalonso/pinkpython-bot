# Pink Python Bot
A python bot which needs to be feeded :snake:

## Requirements

- Python3
- pip
- A twitter app account
- An Api.ai account (in case of use it as NLP)

## Installation

    git clone https://github.com/mtnalonso/pinkpython-bot.git
    cd pinkpython-bot
    pip install -r requirements.txt

Create a credentials.py file as follows:

    CONSUMER_KEY = 'YOUR_TWITTER_CONSUMER_KEY'
    CONSUMER_SECRET = 'YOUR_TWITTER_CONSUMER_SECRET_KEY'
    ACCESS_TOKEN = 'YOUT_TWITTER_ACCESS_TOKEN'
    ACCESS_TOKEN_SECRET = 'YOUT_TWITTER_ACCESS_TOKEN_SECRET'

    # only necessary if using API.ai
    APIAI_ACCESS_TOKEN_DEVELOPER = 'YOUR_APIAI_DEV_TOKEN'
    APIAI_ACCESS_TOKEN_CLIENT = 'YOUR_APIAI_PROD_TOKEN'

## Run

    cd pinkpython
    python3 pinkpython.py
