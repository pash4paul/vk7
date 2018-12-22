# coding: utf8

import logging


def make_execute_method(method_name, **params):
    s = 'API.{method_name}({params})'
    params = str(params).replace(" ", "").replace("'", "\"")
    return s.format(method_name=method_name, params=params)


def make_execute_code(methods):
    return 'return [{}];'.format(','.join(methods))


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
