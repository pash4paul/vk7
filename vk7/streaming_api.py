# coding: utf8

from functools import lru_cache
from typing import Dict, List

import requests
import websocket

from vk7 import VkApi


class StreamingApi(VkApi):
    @lru_cache(maxsize=1)
    def get_streaming_api_credentials(self):
        data = self.streaming.getServerUrl()
        return {
            'endpoint': data['response']['endpoint'],
            'key': data['response']['key']
        }

    @lru_cache(maxsize=1)
    def get_rules_url(self) -> str:
        credentials = self.get_streaming_api_credentials()
        return 'https://{}/rules?key={}'.format(
            credentials['endpoint'],
            credentials['key']
        )

    def add_rule(self, value: str, tag: str) -> Dict:
        params = {
            'rule': {
                'value': value,
                'tag': tag
            }
        }
        return requests.post(self.get_rules_url, json=params).json()

    def get_rules(self) -> List:
        return requests.get(self.get_rules_url).json()['rules'] or []

    def remove_rule(self, tag: str) -> Dict:
        params = {
            'tag': tag
        }
        return requests.delete(self.get_rules_url, json=params).json()

    def get_stream(self, on_open, on_close, on_message, on_error):
        websocket.enableTrace(False)
        credentials = self.get_streaming_api_credentials()

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
