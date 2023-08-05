import os
from urllib.parse import urlencode

import requests

from ..models import UserInfo, InvalidProviderAccessToken
from ..utils import lazy_remote_file


def get_facebook_userinfo(credentials):
    response = requests.get(
        'https://graph.facebook.com/v3.2/me?' + urlencode({
            'access_token': credentials['access_token'],
            'fields': 'id,email,first_name,last_name',
            'format': 'json'
        })
    )

    if not response.ok:
        try:
            data = response.json()
        except Exception:
            raise RuntimeError('Invalid response from Facebook server')

        if data['error']['code'] == 190:
            raise InvalidProviderAccessToken()
        else:
            raise RuntimeError(data['error']['message'])

    data = response.json()

    if not data.get('email'):
        raise RuntimeError('Email not provided by Facebook')

    photo = None
    if data.get('picture'):
        (_, ext) = os.path.splitext(data['picture']['data']['url'])
        name = ''.join(('fb-', data['id'], ext))

        photo = lazy_remote_file(data['picture']['data']['url'], name=name)

    return UserInfo(
        id=data['id'],
        email=data['email'],
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        photo=photo
    )
