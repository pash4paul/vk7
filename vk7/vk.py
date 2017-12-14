#!/usr/bin/env python3
# coding: utf8

from functools import partial
import re
from urllib.parse import urlparse, parse_qsl

import requests


class VK(object):

    def __init__(
            self,
            username=None,
            password=None,
            client_id=None,
            scope=None,
            version='5.69',
            access_token=None,
    ):

        default_scope = [
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
        ]

        self._username = username
        self._password = password,
        self._client_id = client_id
        self._scope = scope or ','.join(default_scope)
        self._version = version
        self._access_token = access_token

        self._api_object_name = None

    def __getattr__(self, method_name):

        if not self._api_object_name:
            self._api_object_name = method_name
            return self

        method_name = '{}.{}'.format(self._api_object_name, method_name)
        self._api_object_name = None

        return partial(self._call_method, method_name)

    def __call__(self, method_name, **params):
        return getattr(self, method_name)(**params)

    def _get_auth_session(self):

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

    def _get_access_token(self):

        if (not self._access_token
            and self._username
            and self._password
        ):
            session = self._get_auth_session()

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
            self._access_token = dict(parse_qsl(query))['access_token']

        return self._access_token

    def _call_method(self, method_name, **params):

        api_url = 'https://api.vk.com/method/{}'.format(method_name)

        access_token = self._get_access_token()
        if access_token:
            params['access_token'] = access_token

        params['v'] = self._version

        data = requests.post(api_url, params).json()
        return data

    def execute(self, **params):
        return self._call_method('execute', **params)
