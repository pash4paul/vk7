#!/usr/bin/env python3
# coding: utf8

import unittest

from vk7 import VK
from vk7.utils import execute_make_method


class TestVk(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.vk = VK()

    def test_call_method(self):
        correct = {
            'response':
                [
                    {
                        'id': 1,
                        'first_name': 'Pavel',
                        'last_name': 'Durov'
                    },
                    {
                        'id': 2,
                        'hidden': 1,
                        'first_name': 'Alexandra',
                        'last_name': 'Vladimirova'
                    }
                ]
        }

        response = self.vk.users.get(user_ids='1,2', lang='en')

        self.assertDictEqual(response, correct)

    def test_make_method_for_execute(self):
        correct = 'API.users.get({"user_ids":"1,2,3"})'

        output = execute_make_method(
            'users.get',
            user_ids='1,2,3'
        )

        self.assertEqual(output, correct)
