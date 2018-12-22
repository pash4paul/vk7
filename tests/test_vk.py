#!/usr/bin/env python3
# coding: utf8

import unittest

from vk7 import Vk
from vk7.utils import make_execute_method


class TestVk(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.vk = Vk()

    def test_make_method_for_execute(self):
        correct = 'API.users.get({"user_ids":"1,2,3"})'

        output = make_execute_method(
            'users.get',
            user_ids='1,2,3'
        )

        self.assertEqual(output, correct)
