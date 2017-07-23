FROM debian:latest
RUN apt-get update -y

# Python
RUN apt-get install -y python3 python3-pip build-essential software-properties-common python-software-properties
RUN pip3 install --upgrade pip

# Project
RUN mkdir ~/pinkpython-bot/
ADD . ~/pinkpython-bot/
WORKDIR ~/pinkpython-bot/
RUN pip3 install -r requirements.txt

CMD python3 twitter_snake.py
