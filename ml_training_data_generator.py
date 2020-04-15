#!/usr/bin/env python
import time, datetime, os, requests, sys, json
# from auth import get_token as get_token
from conf import api
import praw
from pprint import pprint as print


uname=api()['USERNAME']
password=api()['PW']
url="https://reddit.com/"
REDDITOR='username'

BASE_HEADERS = {"User-Agent": "grabber/0.1 by levelxplane"}

def help():
    print ("helper")

if __name__ == '__main__':
    reddit = praw.Reddit(
        client_id=api()['KEY'],
        client_secret=api()['SECRET'],
        user_agent=BASE_HEADERS
    )

    open('comments.txt', 'w')

    for comment in reddit.redditor(REDDITOR).comments.new(limit=None):

        tmp_comment = comment.body
        with open('comments.txt', 'a') as tmp_file:
            tmp_file.write(
                tmp_comment.replace('\n',' ') + '\n'
            )

        # exit(0)
