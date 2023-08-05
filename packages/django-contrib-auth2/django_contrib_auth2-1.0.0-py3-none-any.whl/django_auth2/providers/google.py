import os

import requests

from ..models import InvalidProviderAccessToken, UserInfo
from ..utils import lazy_remote_file


def get_google_userinfo(credentials):
    response = requests.get(
        'https://www.googleapis.com/oauth2/v2/userinfo',
        headers={
            'Authorization': 'Bearer ' + credentials['access_token']
        }
    )

    if not response.ok:
        try:
            data = response.json()
        except Exception:
            raise RuntimeError('Invalid response from google server')

        if data['error'] == 'invalid_grant':
            raise InvalidProviderAccessToken()
        else:
            raise RuntimeError('Invalid response from google server')

    data = response.json()

    photo = None
    if data.get('picture'):
        (_, ext) = os.path.splitext(data['picture'])
        name = ''.join(('g-', data['id'], ext))

        photo = lazy_remote_file(data['picture'], name=name)

    return UserInfo(
        id=data['id'],
        email=data['email'],
        first_name=data.get('given_name'),
        last_name=data.get('family_name'),
        photo=photo
    )
