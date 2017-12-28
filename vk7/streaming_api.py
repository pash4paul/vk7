#!/usr/bin/env python3
# coding: utf8


from typing import Dict, List

import requests
import websocket

from vk7.utils import Lazy, get_streaming_api_credentials


class StreamingApi(object):
    def __init__(self, access_token: str):
        self._credentials = Lazy(lambda: get_streaming_api_credentials(access_token))

    @property
    def rules_url(self) -> str:
        if not hasattr(self, '_rules_url'):
            credentials = self._credentials.value
            self._rules_url = 'https://{}/rules?key={}'.format(
                credentials['endpoint'],
                credentials['key']
            )
        return self._rules_url

    def add_rule(self, value: str, tag: str) -> Dict:
        params = {
            'rule': {
                'value': value,
                'tag': tag
            }
        }

        return requests.post(self.rules_url, json=params).json()

    def get_rules(self) -> List:
        return requests.get(self.rules_url).json()['rules'] or []

    def remove_rule(self, tag: str) -> Dict:
        params = {
            'tag': tag
        }
        return requests.delete(self.rules_url, json=params).json()

    def get_stream(self, on_open, on_close, on_message, on_error):
        websocket.enableTrace(False)
        credentials = self._credentials.value

        url = 'wss://{}/stream?key={}'.format(
            credentials['endpoint'], credentials['key'])

        ws = websocket.WebSocketApp(
            url,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
        )

        ws.on_open = on_open
        ws.run_forever()
