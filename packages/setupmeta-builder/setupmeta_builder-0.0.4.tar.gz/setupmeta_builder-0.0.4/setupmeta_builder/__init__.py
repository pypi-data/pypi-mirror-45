# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

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
    from setuptools import setup
    setup(**setup_attrs)
