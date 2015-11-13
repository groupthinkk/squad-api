import json
import requests

from urllib.parse import urljoin


URL = 'https://api.instagram.com/v1/'
CLIENT_ID = '16cb3dfa6514487eaa5793e30d753db8'


class InstagramAPIError(Exception):
    pass


class InstagramAPIRateLimit(Exception):
    pass


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

    if r.status_code != 200:
        raise InstagramAPIError(r.text)

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


def get_follows(user_id):
    next_url = None

    while True:
        if next_url is not None:
            r = requests.get(next_url)
        else:
            r = requests.get(
                urljoin(URL, 'users/{0}/follows'.format(user_id)),
                params={
                    'client_id': CLIENT_ID,
                    'count': 150,
                    'next_url': next_url,
                },
            )

        if r.status_code == 429:
            yield (None, InstagramAPIRateLimit(r.text))
        elif r.status_code != 200:
            yield (None, InstagramAPIError(r.text))

        data = r.json()

        if not data['data']:
            return

        for user_data in data['data']:
            yield (user_data, None)

        if 'next_url' not in data['pagination']:
            return

        next_url = data['pagination']['next_url']
