# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import sys

from .core import SetupAttrContext, SetupMetaBuilder

def get_setup_attrs(root_path=None) -> dict:
    '''
    get the auto generated attrs dict.
    '''
    ctx = SetupAttrContext(root_path)
    SetupMetaBuilder().fill_ctx(ctx)
    return ctx.setup_attrs

def setup_it(**attrs):
    '''
    just enjoy the auto setup!
    '''
    setup_attrs = get_setup_attrs()
    setup_attrs.update(attrs)

    def print_attrs():
        setup_attrs_copy = setup_attrs.copy()
        from prettyprinter import pprint
        long_description = setup_attrs.get('long_description')
        if long_description and len(long_description) > 205:
            setup_attrs_copy['long_description'] = long_description[:200] + '...'
        pprint(setup_attrs_copy)

    from setuptools import setup
    from distutils.cmd import Command

    class PrintAttrs(Command):
        def _empty(self):
            pass

        user_options = []
        initialize_options = _empty
        finalize_options = _empty

        def run(self):
            print_attrs()

    setup_attrs.setdefault('cmdclass', {}).update({
        'print_attrs': PrintAttrs
    })
    setup(**setup_attrs)
