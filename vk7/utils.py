#!/usr/bin/env python3
# coding: utf8

import functools
import logging
import re
from typing import Dict
from urllib.parse import urlparse, parse_qsl

import requests


class Lazy(object):
    def __init__(self, factory_func):
        self._factory_func = factory_func

    @property
    def value(self):
        if not hasattr(self, '_value'):
            self._value = self._factory_func()
        return self._value


def compose(*functions):
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)


def execute_make_method(method_name, **params):
    s = 'API.{method_name}({params})'
    params = str(params).replace(" ", "").replace("'", "\"")
    return s.format(method_name=method_name, params=params)


def execute_make_code(methods):
    return 'return [{}];'.format(','.join(methods))


def offsets_iterator(offset, total, batch_size):
    res = []
    for i in range(offset, total+offset, offset):
        res.append(i)
        if len(res) == batch_size:
            yield res
            res = []
    yield res


def get_logger(name):

    level = logging.INFO

    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)

    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(ch)

    return logger


def get_auth_session(username, password):

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
        'email': username,
        'pass': password
    }
    session.post(auth_url, data)
    return session


def get_access_token(username, password, client_id, scope=None, version='5.69'):

    scope = scope or [
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

    session = get_auth_session(username, password)

    auth_api_url = 'https://oauth.vk.com/authorize'
    re_token_url = re.compile(r'https://login.vk.com/[?]act=grant_access.*?&https=1')

    params = {
        'client_id': client_id,
        'display': 'page',
        'redirect_uri': 'https://oauth.vk.com/blank.html',
        'scope': scope,
        'response_type': 'token',
        'v': version
    }

    response = session.get(auth_api_url, params=params)

    if 'access_token' not in response.url:
        html = response.text
        url = re.findall(re_token_url, html)[0]
        response = session.get(url)

    query = urlparse(response.url).fragment
    access_token = dict(parse_qsl(query))['access_token']

    return access_token


def get_streaming_api_credentials(access_token: str) -> Dict:
    from vk7 import VK

    data = VK(access_token=access_token).streaming.getServerUrl()
    return {
        'endpoint': data['response']['endpoint'],
        'key': data['response']['key']
    }
