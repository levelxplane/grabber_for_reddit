# Just some random scripts playing around with PRAW
Python 3

# Environment
In your .bashrc or .zshrc add the following:

`export REDDIT_USERNAME=<your username>`

`export REDDIT_PASSWORD=<your password>`


# Instructions - Local
After cloning and moving into directory:

`virutalenv env`

`source env/usr/local/bin/activate` (or `source env/bin/activate`)

`pip install -r requirements.txt`

`python <script>.py`


# Instructions - Docker
`docker-compose build`

`docker-compose up`

`docker exec -it grabber_app bash`

`python <script>.py`


# Scripts

`ml_training_data_generator.py` for use with https://colab.research.google.com/drive/1VLG8e7YSEwypxU-noRNhsv5dW4NfTGce

`common_subs.py` for finding common subreddits among users from a certain other subreddit
