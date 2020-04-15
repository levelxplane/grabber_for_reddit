#!/usr/bin/env python
import time, datetime, os, requests, sys, json
from conf import api

uname=api()['USERNAME']
password=api()['PW']
url="https://oauth.reddit.com/api/v1/"

def base_headers():
    return {"User-Agent": "reddscript/0.1 by levelxplane"}


def create_token():
    client_auth = requests.auth.HTTPBasicAuth(api()['KEY'], api()['SECRET'])
    post_data = {"grant_type": "password",
                 "username": uname, "password": password}
    headers = base_headers()
    response = requests.post("https://www.reddit.com/api/v1/access_token",
                             auth=client_auth, data=post_data, headers=headers)

    newfile = open('token.txt', 'w')
    # print (uname, password)
    newfile.write(str(response.json()['access_token']))
    newfile.close()

    return str(response.json()['access_token'])

def get_token():
    try:
        with open('token.txt', 'r') as tokenfile:
            tmp = tokenfile.read()
            if check_user(tmp) is 200:
                return tmp
            else:
                return create_token()
    except Exception as e:
        print (e)
        exit(0)
        return create_token()

def check_user(token):
    headers=base_headers()
    headers.update({"Authorization":"bearer " + token })
    response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
    return response.status_code

# print (get_token())
# print (token)

# auth_header = {"Authorization": "bearer "+get_token(), "User-Agent": "ChangeMeClient/0.1 by levelxplane"}
# req=requests.get(url+"me", headers=auth_header)
# print(req.json())
