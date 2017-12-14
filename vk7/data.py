#!/usr/bin/env python3
# coding: utf8

from vk7.utils import (
    execute_make_method,
    execute_make_code,
    offsets_iterator,
    get_logger
)


logger = get_logger(__name__)


def objects_iterator(vk, method, params, total, verbose=False):

    for offsets in offsets_iterator(100, total, 25):

        if verbose:
            logger.info('{} {}'.format(method, offsets[-1]))

        methods = [
            execute_make_method(method, offset=offset, count=100, **params)
            for offset in offsets
        ]

        code = execute_make_code(methods)
        data = vk.execute(code=code)

        for batch in data['response']:
            for item in batch['items']:
                yield item


def group_members_iterator(vk, group_id, fields='sex', verbose=False):

    method = 'groups.getMembers'

    params = {
        'group_id': group_id,
        'sort': 'id_asc',
        'fields': fields
    }

    data = vk.groups.getMembers(offset=0, count=0, **params)
    total_members = data['response']['count']

    return objects_iterator(vk, method, params, total_members, verbose)


def docs_iterator(vk, q, verbose=False):

    method = 'docs.search'

    params = {
        'q': q
    }

    return objects_iterator(vk, method, params, 1000, verbose)
