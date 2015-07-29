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
        if user['username'] == username:
            return user


def get_posts(user_id):
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
            break

        for post in data:
            max_id = post['id']
            yield post
