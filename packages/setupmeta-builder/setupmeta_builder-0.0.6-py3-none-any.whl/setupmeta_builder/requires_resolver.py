# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from abc import abstractmethod, ABC

import pkg_resources


class RequiresResolver(ABC):
    @property
    @abstractmethod
    def name(self):
        raise NotImplementedError

    @abstractmethod
    def resolve_install_requires(self, ctx) -> list:
        raise NotImplementedError

    @abstractmethod
    def resolve_tests_require(self, ctx) -> list:
        raise NotImplementedError

    def _sorted_list(self, ls):
        return list(sorted(ls))


class RequirementsTxtRequiresResolver(RequiresResolver):
    @property
    def name(self):
        return 'requirements.txt'

    @staticmethod
    def _package_to_require(pkg_info: pkg_resources.Requirement):
        return pkg_info.name

    def resolve_install_requires(self, ctx) -> list:
        requirements = ctx.get_text_content('requirements.txt')
        if requirements is None:
            return None

        return self._sorted_list(
            [self._package_to_require(r) for r in pkg_resources.parse_requirements(requirements)]
        )

    def resolve_tests_require(self, ctx) -> list:
        return None


class PipfileRequiresResolver(RequiresResolver):
    @property
    def name(self):
        return 'Pipfile'

    def _get_pipfile(self, ctx):
        if 'pipfile' not in ctx.state:
            pipfile_path = ctx.root_path / 'Pipfile'
            if pipfile_path.is_file():
                import pipfile
                pf = pipfile.load(str(pipfile_path))
            else:
                pf = None
            ctx.state['pipfile'] = pf
        return ctx.state['pipfile']

    @staticmethod
    def _package_to_require(k, v):
        if v == '*':
            return k
        raise NotImplementedError((k, v))

    def _resolve_requires(self, ctx, attr_name, pf_key):
        pf = self._get_pipfile(ctx)
        if pf is None:
            return None
        requires = []
        for k, v in pf.data[pf_key].items():
            requires.append(self._package_to_require(k, v))
        return self._sorted_list(requires)

    def resolve_install_requires(self, ctx) -> list:
        return self._resolve_requires(ctx, 'install_requires', 'default')

    def resolve_tests_require(self, ctx) -> list:
        return self._resolve_requires(ctx, 'tests_require', 'develop')


class ChainRequiresResolver(RequiresResolver):
    def __init__(self, *resolvers):
        self.resolvers = list(resolvers)

    @property
    def name(self):
        childs_name = ', '.join([c.name for c in self.resolvers])
        return f'chain({childs_name})'

    def resolve_install_requires(self, ctx) -> list:
        for r in self.resolvers:
            ret = r.resolve_install_requires(ctx)
            if ret is not None:
                return ret

    def resolve_tests_require(self, ctx) -> list:
        for r in self.resolvers:
            ret = r.resolve_tests_require(ctx)
            if ret is not None:
                return ret


class StrictRequiresResolver(RequiresResolver):
    def __init__(self, *resolvers):
        self.resolvers = list(resolvers)

    @property
    def name(self):
        childs_name = ', '.join([c.name for c in self.resolvers])
        return f'strict({childs_name})'

    def _get_result(self, rets: list):
        rets = [r for r in rets if r[1] is not None]
        if not rets:
            return None
        rslr, ret = rets[0]
        for orslr, oret in rets[1:]:
            if oret != ret:
                msg = '\n'.join([
                    f'{rslr.name} report: {ret!r}',
                    f'{orslr.name} report: {oret!r}',
                ])
                raise RuntimeError('different result from multi source: \n' + msg)
        return ret

    def resolve_install_requires(self, ctx) -> list:
        rets = [(r, r.resolve_install_requires(ctx)) for r in self.resolvers]
        return self._get_result(rets)

    def resolve_tests_require(self, ctx) -> list:
        rets = [(r, r.resolve_tests_require(ctx)) for r in self.resolvers]
        return self._get_result(rets)


class DefaultRequiresResolver(RequiresResolver):
    def __init__(self):
        self._install_resolver = StrictRequiresResolver(
            RequirementsTxtRequiresResolver(),
            PipfileRequiresResolver()
        )
        self._test_resolver = StrictRequiresResolver(
            PipfileRequiresResolver()
        )

    @property
    def name(self):
        return 'default'

    def resolve_install_requires(self, ctx) -> list:
        return self._install_resolver.resolve_install_requires(ctx)

    def resolve_tests_require(self, ctx) -> list:
        return self._test_resolver.resolve_tests_require(ctx)
