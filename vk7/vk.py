# coding: utf8

from functools import partial

import requests

from vk7.utils import Lazy
from vk7.common import get_access_token


class VK(object):

    def __init__(self, username: str=None, password: str=None,
                 client_id: int=None, scope: str=None, version: str='5.71',
                 access_token: str=None):

        if username and password and client_id:
            self._access_token = Lazy(
                lambda: get_access_token(username, password, client_id,
                                         scope, version))
        else:
            self._access_token = Lazy(lambda: access_token)

        self._version = version

        self._call_stack = []
        self._max_stack_size = 2

    def __getattr__(self, method):

        self._call_stack.append(method)

        if len(self._call_stack) == self._max_stack_size or method == 'execute':
            method = '.'.join(self._call_stack)
            self._call_stack = []
            return partial(self._call, method)
        else:
            return self

    def __call__(self, method, **params):
        return getattr(self, method)(**params)

    def _call(self, method, **params):

        api_url = 'https://api.vk.com/method/{}'.format(method)

        params.update({
            'access_token': self._access_token.value,
            'v': self._version
        })

        data = requests.post(api_url, params).json()
        return data
