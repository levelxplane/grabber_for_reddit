#!/usr/bin/env python
import time, datetime, os, requests, sys, json, operator
from os import path
from conf import api
import praw
# from pprint import pprint as print

UNAME=api()['USERNAME']
PWORD=api()['PW']
URL="https://reddit.com/"

SUBREDDIT='wallstreetbets'      # sub to inspect
THREAD_COUNT=1              # number of top posts to use as sample size
PERIOD='month'               # period of length for sample size. can be hour, day, month, all

COMMENT_LIMIT=50               # number of comments to use from users found in threads

BASE_HEADERS = {"User-Agent": "grabber/0.1 by levelxplane"}

UNIQUE_USERS = set()
COMMON_SUBS = {}

def traverse_sub(reddit_client):
    open('user_generation_error.log', 'w')      # clears error log

    for submission in reddit_client.subreddit(SUBREDDIT).top(limit=THREAD_COUNT, time_filter=PERIOD):
        UNIQUE_USERS.add(submission.author.name)

        grab_users(submission.comments.list())      # converts forest to flat list

    with open ('users_from_{}.csv'.format(SUBREDDIT), 'a+') as user_file:
        for username in UNIQUE_USERS:
            user_file.write(username+'\n')


def grab_users(flat_list):
    for comment_object in flat_list:
        try:
            if type(comment_object) == praw.models.reddit.more.MoreComments:
                grab_users(comment_object.comments())
            elif type(comment_object) == praw.models.comment_forest.CommentForest:
                grab_users(comment.comments.list())
            elif type(comment_object) == praw.models.reddit.comment.Comment:
                uname = comment_object.author.name
                if uname:
                    UNIQUE_USERS.add(uname)
            else:
                continue
        except Exception as e:
            with open('user_generation_error.log', 'a') as err_file:
                err_file.write(','.join([
                    str(type(comment_object)),
                    str(comment_object),
                    str(e)
                ])+'\n')

def get_subs_from_users(reddit_client):
    open('commonsub_generation_error.log', 'w')

    with open('users_from_{}.csv'.format(SUBREDDIT), 'r') as user_file:
        users = user_file.readlines()

    users = [x.rstrip() for x in users]

    for count, username in enumerate(users):
        user = reddit.redditor(username)
        print(str(count), '/', str(len(users)))

        for comment in user.comments.new(limit=COMMENT_LIMIT):
            # sub = comment.subreddit.name
            sub = comment.subreddit.display_name
            if sub != SUBREDDIT:
                try:
                    COMMON_SUBS[sub] += 1
                except KeyError:
                    COMMON_SUBS[sub] = 1

    with open('common_subs_from_{}.json'.format(SUBREDDIT), 'w') as json_file:
        json.dump(COMMON_SUBS, json_file)

# if you're a chad and got name(t5_kj4l32) instead of display_name(r/spacedicks) from subreddit
def get_subname_from_id(reddit_client):
    tmp_dict = {}
    with open('common_subs_from_{}.json'.format(SUBREDDIT), 'r') as common_sub_file:
        common_subs = json.loads(common_sub_file.read())

    progress = 0
    for sub_t5, count in common_subs.items():
        progress+=1
        # subreddit_obj = reddit_client.subreddit(name=sub)
        # print(subreddit_obj.display_name)
        res = list(reddit_client.info([sub_t5]))
        actual_name = res[0].display_name

        print ('{} / {}'.format(progress, len(common_subs)))

        tmp_dict[actual_name] = count

    with open('new_common_subs_from_{}.json'.format(SUBREDDIT), 'w+') as common_sub_file:
        json.dump(tmp_dict, common_sub_file)
        # response = requests.get(URL+'/r/{}/about.json'.format(SUBREDDIT), headers=BASE_HEADERS)
        # print (response.json()['data']['display_name'])

def generate_report():
        with open('common_subs_from_{}.json'.format(SUBREDDIT), 'r') as common_sub_file:
            common_subs = json.loads(common_sub_file.read())

        sorted_tuples = []
        for sub, count in common_subs.items():
            sorted_tuples.append((sub, count))

        sorted_tuples.sort(key = operator.itemgetter(1))
        for x in sorted_tuples[::-1][1:21]:
            print(x)
        #
        # for x in sorted_tuples.reverse():
        #     print (x)

if __name__ == '__main__':
    reddit = praw.Reddit(
        client_id=api()['KEY'],
        client_secret=api()['SECRET'],
        user_agent=BASE_HEADERS
    )

    if not os.path.exists('users_from_{}.csv'.format(SUBREDDIT)):
        traverse_sub(reddit)

    if not os.path.exists('common_subs_from_{}.json'.format(SUBREDDIT)):
        get_subs_from_users(reddit)

    if not os.path.exists('{}_report.csv'.format(SUBREDDIT)):
        # get_subname_from_id(reddit)
        generate_report()
