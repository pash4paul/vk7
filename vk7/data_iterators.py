# coding: utf8

from collections import namedtuple
from typing import Dict

from vk7 import VK
from vk7.utils import (
    execute_make_method,
    execute_make_code,
    get_logger,
    chunks
)

logger = get_logger(__name__)

DynamicParam = namedtuple('IterableParam', 'name,values')


class Execute:
    calls_per_request = 25

    def __init__(self,
                 vk: VK,
                 method: str,
                 params: Dict,
                 dynamic_param: namedtuple,
                 items_key: str='',
                 verbose: bool=False,
                 batch_mode: bool=False):

        self._vk = vk
        self._method = method
        self._params = params
        self._dynamic_param = dynamic_param
        self._items_key = items_key
        self._verbose = verbose
        self._batch_mode = batch_mode

    def print_log(self, params):
        params = ','.join(map(str, params))
        logger.info('{} {}'.format(self._method, params))

    def __iter__(self):
        for values in chunks(
                self._dynamic_param.values, self.calls_per_request
        ):
            if self._verbose:
                self.print_log(values)

            methods = []
            for value in values:
                self._params[self._dynamic_param.name] = value
                methods.append(
                    execute_make_method(self._method, **self._params)
                )

            code = execute_make_code(methods)
            data = self._vk.execute(code=code)

            if 'execute_errors' in data:
                logger.error(data['execute_errors'])

            for batch in data['response']:
                if isinstance(batch, bool):
                    continue

                if self._items_key:
                    batch = batch[self._items_key]

                if self._batch_mode:
                    yield batch
                else:
                    for item in batch:
                        yield item
        raise StopIteration


def group_members_iterator(vk: VK,
                           group_id: int,
                           fields: str= '',
                           verbose=False,
                           batch_mode: bool=False) -> Execute:
    params = {
        'group_id': group_id,
        'sort': 'id_asc',
        'fields': fields
    }

    count = vk.groups.getMembers(
        offset=0, count=0, **params
    )['response']['count']

    params['count'] = 100

    dynamic_param = DynamicParam(
        name='offset',
        values=range(100, count+100, 100)
    )

    return Execute(
        vk, 'groups.getMembers', params, dynamic_param, 'items', verbose,
        batch_mode
    )


def docs_iterator(vk: VK,
                  q: str,
                  verbose: bool=False,
                  batch_mode: bool=False) -> Execute:
    params = {
        'q': q,
        'count': 100
    }

    max_docs_count = 1000

    dynamic_param = DynamicParam(
        name='offset',
        values=range(100, max_docs_count + 100, 100)
    )

    return Execute(
        vk, 'docs.search', params, dynamic_param, 'items', verbose, batch_mode
    )


def users_groups_ids_iterator(vk: VK,
                              users_ids: list,
                              verbose=False,
                              batch_mode: bool=False) -> Execute:
    dynamic_param = DynamicParam(
        name='user_id',
        values=users_ids
    )

    return Execute(
        vk, 'groups.get', {}, dynamic_param, 'items', verbose, batch_mode
    )


def groups_iterator(vk: VK,
                    groups_ids: list,
                    fields: str= '',
                    verbose=False,
                    batch_mode: bool=False) -> Execute:
    dynamic_param = DynamicParam(
        name='group_ids',
        values=groups_ids
    )

    return Execute(
        vk, 'groups.getById', {'fields': fields}, dynamic_param, '', verbose,
        batch_mode
    )


def group_posts_iterator(vk: VK, group_id: int, verbose=False,
                         batch_mode: bool=False) -> Execute:
    params = {
        'owner_id': '-{}'.format(group_id),
    }

    count = vk.wall.get(
        offset=0, count=0, **params
    )['response']['count']

    params['count'] = 100

    dynamic_param = DynamicParam(
        name='offset',
        values=range(100, count + 100, 100)
    )

    return Execute(
        vk, 'wall.get', params, dynamic_param, 'items', verbose, batch_mode
    )
