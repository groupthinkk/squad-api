import json
import requests

from urllib.parse import urljoin


URL = 'https://api.instagram.com/v1/'
CLIENT_ID = '16cb3dfa6514487eaa5793e30d753db8'


def find_user(username):
    r = requests.get(
        urljoin(URL, 'users/search'),
        params={
            'q': username,
            'client_id': CLIENT_ID,
        },
    )

    data = r.json()['data']

    for user in data:
        if user['username'].lower() == username.lower():
            return user


def get_user(user_id):
    r = requests.get(
        urljoin(URL, 'users/{0}'.format(user_id)),
        params={
            'client_id': CLIENT_ID,
        },
    )

    return r.json()['data']


def get_posts(user_id, count=1000):
    i = 0
    max_id = None

    while True:
        r = requests.get(
            urljoin(URL, 'users/{0}/media/recent'.format(user_id)),
            params={
                'count': 150,
                'max_id': max_id,
                'client_id': CLIENT_ID,
            },
        )

        data = r.json()['data']

        if not data:
            return

        for post in data:
            i += 1
            max_id = post['id']
            yield post

        if i >= count:
            return
