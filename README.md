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

    consumer_key = 'YOUR_TWITTER_CONSUMER_KEY'
    consumer_secret = 'YOUR_TWITTER_CONSUMER_SECRET_KEY'
    access_token = 'YOUT_TWITTER_ACCESS_TOKEN'
    access_token_secret = 'YOUT_TWITTER_ACCESS_TOKEN_SECRET'

    # only necessary if using API.ai
    apiai_access_token_developer = 'YOUR_APIAI_DEV_TOKEN'
    apiai_access_token_client = 'YOUR_APIAI_PROD_TOKEN'

## Run

    cd pinkpython
    python3 pinkpython.py
