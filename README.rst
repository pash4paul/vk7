================================================================
Framework for extract data from vk.com (russian social network).
================================================================

This is a framework for extract data from vk.com (russian social network).
The goal is to give helpful interface for work with api and extracting data.

Quickstart
==========

Install
-------

.. code:: bash

    pip install vk7

Usage
-----

.. code:: python

    >>> from vk7 import Vk
    >>>
    >>> vk = VK('username', 'password', 'client_id')
    >>> vk.users.get(user_ids='1,2')
    {'response': [{'id': 1, 'first_name': 'Павел', 'last_name': 'Дуров'}, {'id': 2, 'first_name': 'Александра', 'last_name': 'Владимирова'}]}

    >>>
    >>> items = vk.groups.getMembers(group_id=1, fields='bdate,sex')
    >>> item = next(items)
    >>> item
    {'id': 5, 'first_name': 'Илья', 'last_name': 'Перекопский', 'sex': 2, 'bdate': '18.11'}

See https://vk.com/dev/methods for detailed API guide.
