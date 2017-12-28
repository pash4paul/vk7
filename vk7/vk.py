#!/usr/bin/env python3
# coding: utf8

from functools import partial

import requests

from vk7.utils import get_access_token, Lazy


class VK(object):

    def __init__(self, username=None, password=None, client_id=None, scope=None, version='5.69', access_token=None):

        if username and password and client_id:
            self._access_token = Lazy(lambda: get_access_token(username, password, client_id, scope, version))
        else:
            self._access_token = Lazy(lambda: access_token)

        self._version = version

        self._call_stack = []
        self._max_stack_size = 2

    def __getattr__(self, method_name):

        self._call_stack.append(method_name)

        if len(self._call_stack) == self._max_stack_size or method_name == 'execute':
            method_name = '.'.join(self._call_stack)
            self._call_stack = []
            return partial(self._call_method, method_name)
        else:
            return self

    def __call__(self, method_name, **params):
        return getattr(self, method_name)(**params)

    def _call_method(self, method_name, **params):
        api_url = 'https://api.vk.com/method/{}'.format(method_name)

        params.update({
            'access_token': self._access_token.value,
            'v': self._version
        })

        data = requests.post(api_url, params).json()
        return data
