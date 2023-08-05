# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
import json
from pathlib import Path
from collections import ChainMap

from .requires_resolver import DefaultRequiresResolver

class SetupAttrContext:
    def __init__(self, root_path=None):
        self._setup_attrs = {}
        self._root_path = Path(root_path) if root_path else Path.cwd()
        self._state = {}
        self._pkgit_conf: dict = None

    @property
    def setup_attrs(self):
        return self._setup_attrs

    @property
    def root_path(self):
        return self._root_path

    @property
    def state(self):
        '''
        a dict for store cached state.
        '''
        return self._state

    def get_text_content(self, relpath) -> str:
        '''get file or None'''
        path = self._root_path / relpath
        if path.is_file():
            return path.read_text('utf-8')

    def get_pkgit_conf(self) -> dict:
        if self._pkgit_conf is None:
            global_conf_path = Path.home() / '.pkgit.json'
            if global_conf_path.is_file():
                global_conf = json.loads(global_conf_path.read_text('utf-8'))
            else:
                global_conf = {}

            cwd_conf_text = self.get_text_content('.pkgit.json')
            if cwd_conf_text:
                cwd_conf = json.loads(cwd_conf_text)
            else:
                cwd_conf = {}

            self._pkgit_conf = ChainMap(cwd_conf, global_conf)

        return self._pkgit_conf


class SetupMetaBuilder:
    will_update_attrs = [
        'packages',
        'long_description',
        'name',
        'version',
        'author',
        'author_email',
        'url',
        'license',
        'classifiers',
        'scripts',
        'entry_points',
        'zip_safe',
        'include_package_data',
        'setup_requires',
        'install_requires',
        'tests_require',
    ]

    def __init__(self):
        self.requires_resolver = DefaultRequiresResolver()

    def fill_ctx(self, ctx: SetupAttrContext):
        for attr in self.will_update_attrs:
            if attr not in ctx.setup_attrs:
                getattr(self, f'update_{attr}')(ctx)

    def update_packages(self, ctx: SetupAttrContext):
        from setuptools import find_packages

        ctx.setup_attrs['packages'] = find_packages(where=str(ctx.root_path))

    def update_long_description(self, ctx: SetupAttrContext):
        rst = ctx.get_text_content('README.rst')
        if rst is not None:
            ctx.setup_attrs['long_description'] = rst
            return

        md = ctx.get_text_content('README.md')
        if md is not None:
            ctx.setup_attrs['long_description'] = md
            ctx.setup_attrs['long_description_content_type'] = 'text/markdown'
            return

        ctx.setup_attrs.setdefault('long_description', '')

    def update_name(self, ctx: SetupAttrContext):
        packages = ctx.setup_attrs.get('packages')
        if packages and len(packages) == 1:
            ctx.setup_attrs['name'] = packages[0]

    def update_version(self, ctx: SetupAttrContext):
        pass

    def update_author(self, ctx: SetupAttrContext):
        author = ctx.get_pkgit_conf().get('author')
        if author:
            ctx.setup_attrs['author'] = author

    def update_author_email(self, ctx: SetupAttrContext):
        author_email = ctx.get_pkgit_conf().get('author_email')
        if author_email:
            ctx.setup_attrs['author_email'] = author_email

    def update_url(self, ctx: SetupAttrContext):
        import subprocess
        def get_url_from_remote(name):
            git_remote_get_url = subprocess.run(
                ['git', 'remote', 'get-url', name],
                stdout=subprocess.PIPE, encoding='utf-8'
            )
            if git_remote_get_url.returncode != 0:
                return
            return git_remote_get_url.stdout.strip()

        git_remote = subprocess.run(['git', 'remote'], stdout=subprocess.PIPE, encoding='utf-8')
        if git_remote.returncode != 0:
            return
        lines = git_remote.stdout.strip().splitlines()
        if 'origin' in lines:
            git_url = get_url_from_remote('origin')
        else:
            git_url = None

        if git_url:
            from .utils import parse_url_from_git_https, parse_url_from_git_ssh
            if git_url.startswith('git@'):
                url = parse_url_from_git_ssh(git_url)
            else:
                url = parse_url_from_git_https(git_url)
            ctx.setup_attrs['url'] = url


    def update_license(self, ctx: SetupAttrContext):
        lice = ctx.get_text_content('LICENSE')
        if not lice:
            return

        from .licenses import LICENSES

        lines = lice.splitlines()
        if lines[0] in LICENSES:
            ctx.setup_attrs['license'] = lines[0]

    def update_classifiers(self, ctx: SetupAttrContext):
        # see: https://pypi.org/classifiers/
        ctx.setup_attrs['classifiers'] = classifiers = []

        from .licenses import LICENSES_CLASSIFIERS_MAP
        lice = ctx.setup_attrs.get('license')
        if lice and lice in LICENSES_CLASSIFIERS_MAP:
            classifiers.append(
                LICENSES_CLASSIFIERS_MAP[lice]
            )

    def update_scripts(self, ctx: SetupAttrContext):
        pass

    def update_entry_points(self, ctx: SetupAttrContext):
        pass

    def update_zip_safe(self, ctx: SetupAttrContext):
        ctx.setup_attrs['zip_safe'] = False

    def update_include_package_data(self, ctx: SetupAttrContext):
        ctx.setup_attrs['include_package_data'] = True

    def update_setup_requires(self, ctx: SetupAttrContext):
        pass

    def update_install_requires(self, ctx: SetupAttrContext):
        self.requires_resolver.resolve_install_requires(ctx)

    def update_tests_require(self, ctx: SetupAttrContext):
        self.requires_resolver.resolve_tests_require(ctx)
