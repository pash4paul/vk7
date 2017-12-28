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

    >>> from vk7 import VK
    >>> from vk7.data_iterators import group_members_iterator
    >>>
    >>> vk = VK()
    >>> vk.users.get(user_ids='1,2')
    {'response': [{'first_name': 'Павел', 'id': 1, 'last_name': 'Дуров'},
      {'first_name': 'Александра',
       'hidden': 1,
       'id': 2,
       'last_name': 'Владимирова'}]}
    >>>
    >>> vk = VK('username', 'password', 'client_id')
    >>> fields = ('bdate', 'connections', 'domain', 'followers_count', 'sex')
    >>> group_members = group_members_iterator(vk, 'group_id', ','.join(fields), verbose=True)

See https://vk.com/dev/methods for detailed API guide.
