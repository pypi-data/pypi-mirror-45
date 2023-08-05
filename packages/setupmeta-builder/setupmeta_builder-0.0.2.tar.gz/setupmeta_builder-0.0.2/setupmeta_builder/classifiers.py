# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
# see: https://pypi.org/classifiers/
# ----------

from abc import abstractmethod, ABC

PY_CLASSIFIERS_MAP = {
    '2': 'Programming Language :: Python :: 2',
    '2.3': 'Programming Language :: Python :: 2.3',
    '2.4': 'Programming Language :: Python :: 2.4',
    '2.5': 'Programming Language :: Python :: 2.5',
    '2.6': 'Programming Language :: Python :: 2.6',
    '2.7': 'Programming Language :: Python :: 2.7',
    '3.0': 'Programming Language :: Python :: 3.0',
    '3.1': 'Programming Language :: Python :: 3.1',
    '3.2': 'Programming Language :: Python :: 3.2',
    '3.3': 'Programming Language :: Python :: 3.3',
    '3.4': 'Programming Language :: Python :: 3.4',
    '3.5': 'Programming Language :: Python :: 3.5',
    '3.6': 'Programming Language :: Python :: 3.6',
    '3.7': 'Programming Language :: Python :: 3.7',
    '3.8': 'Programming Language :: Python :: 3.8',
}

class IClassifierUpdater(ABC):
    All = []

    @abstractmethod
    def update_classifiers(self, ctx, classifiers: list):
        raise NotImplementedError

    def __init_subclass__(cls, *args, **kwargs):
        cls.All.append(cls)


class TravisCIClassifierUpdater(IClassifierUpdater):
    def update_classifiers(self, ctx, classifiers: list):
        # see: https://pypi.org/classifiers/
        travis_yaml = ctx.get_fileinfo('.travis.yml')
        if travis_yaml.is_file():
            travis_conf = travis_yaml.load(format='yaml')
            pylist = travis_conf.get('python', [])
            for py in pylist:
                if py in PY_CLASSIFIERS_MAP:
                    classifiers.append(PY_CLASSIFIERS_MAP[py])
