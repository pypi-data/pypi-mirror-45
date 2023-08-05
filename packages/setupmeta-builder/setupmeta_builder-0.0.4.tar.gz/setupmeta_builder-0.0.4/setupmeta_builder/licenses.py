# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from .classifiers import IClassifierUpdater

LICENSE_MIT = 'MIT License'

LICENSES = {
    LICENSE_MIT
}

LICENSES_CLASSIFIERS_MAP = {
    LICENSE_MIT: 'License :: OSI Approved :: MIT License'
}

class LicenseClassifierUpdater(IClassifierUpdater):
    def update_classifiers(self, ctx, classifiers):
        lice = ctx.setup_attrs.get('license')
        if lice and lice in LICENSES_CLASSIFIERS_MAP:
            classifiers.append(
                LICENSES_CLASSIFIERS_MAP[lice]
            )
