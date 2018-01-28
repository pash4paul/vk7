# coding: utf8

import functools
import logging


class Lazy(object):
    def __init__(self, factory_func):
        self._factory_func = factory_func

    @property
    def value(self):
        if not hasattr(self, '_value'):
            self._value = self._factory_func()
        return self._value


def compose(*functions):
    return functools.reduce(
        lambda f, g: lambda x: f(g(x)), reversed(functions), lambda x: x)


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


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


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
