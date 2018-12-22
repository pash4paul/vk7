# coding: utf8

import re
from functools import partial, lru_cache
from urllib.parse import urlparse, parse_qsl

import requests


class VkApi:
    API_URL = 'https://api.vk.com/method/{}'

    def __init__(self, username: str = None, password: str = None, client_id: int = None, scope: str = None,
                 version: str = '5.71', access_token: str = None):
        self._username = username
        self._password = password
        self._client_id = client_id
        self._scope = scope or ','.join([
            'friends',
            'photos',
            'audio',
            'video',
            'pages',
            'status',
            'notes',
            'messages',
            'wall',
            'offline',
            'docs',
            'groups',
            'notifications',
            'stats',
            'email',
            'market'
        ])
        self._version = version
        self._access_token = access_token

        self._call_stack = []
        self._stack_size = 2

        self._methods = {}

    def get_auth_session(self):
        auth_url = 'https://login.vk.com/?act=login'

        re_ip_h = re.compile(r'name="ip_h" value="([a-z0-9]+)"')
        re_lg_h = re.compile(r'name="lg_h" value="([a-z0-9]+)"')

        session = requests.Session()

        html = session.get(auth_url).text
        ip_h = re.findall(re_ip_h, html)
        lg_h = re.findall(re_lg_h, html)

        data = {
            'act': 'login',
            'role': 'al_frame',
            '_origin': 'https://vk.com',
            'ip_h': ip_h,
            'lg_h': lg_h,
            'email': self._username,
            'pass': self._password
        }
        session.post(auth_url, data)
        return session

    @lru_cache(maxsize=1)
    def get_access_token(self) -> str:
        if self._access_token:
            return self._access_token

        session = self.get_auth_session()

        auth_api_url = 'https://oauth.vk.com/authorize'
        re_token_url = re.compile(r'https://login.vk.com/[?]act=grant_access.*?&https=1')

        params = {
            'client_id': self._client_id,
            'display': 'page',
            'redirect_uri': 'https://oauth.vk.com/blank.html',
            'scope': self._scope,
            'response_type': 'token',
            'v': self._version
        }

        response = session.get(auth_api_url, params=params)

        if 'access_token' not in response.url:
            html = response.text
            url = re.findall(re_token_url, html)[0]
            response = session.get(url)

        query = urlparse(response.url).fragment

        return dict(parse_qsl(query))['access_token']

    def __getattr__(self, method):
        self._call_stack.append(method)

        if len(self._call_stack) == self._stack_size or method == 'execute':
            method = '.'.join(self._call_stack)
            self._call_stack = []
            if '_'.join(method.split('.')) in self._methods:
                return self._methods['_'.join(method.split('.'))]
            return partial(self._call, method)
        else:
            return self

    def __call__(self, method, **params):
        return getattr(self, method)(**params)

    def _call(self, method, **params):
        params.update({
            'access_token': self.get_access_token(),
            'v': self._version
        })
        data = requests.post(self.API_URL.format(method), params).json()
        return data
