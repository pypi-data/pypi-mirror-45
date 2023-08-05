# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------


def parse_url_from_git_ssh(git_url: str):
    # parse git@github.com:Cologler/setupmeta_builder-python.git
    # to https://github.com/Cologler/setupmeta_builder-python
    assert git_url.endswith('.git')
    assert git_url.startswith('git@')
    git_url = git_url[4:-4]
    host, _, path = git_url.partition(':')
    return f'https://{host}/{path}'

def parse_url_from_git_https(git_url: str):
    # parse https://github.com/Cologler/setupmeta_builder-python.git
    # to https://github.com/Cologler/setupmeta_builder-python
    assert git_url.endswith('.git')
    return git_url[:-4]
