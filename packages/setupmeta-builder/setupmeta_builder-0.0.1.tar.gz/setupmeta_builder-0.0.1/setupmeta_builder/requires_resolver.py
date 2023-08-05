# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from abc import abstractmethod, ABC

class RequiresResolver(ABC):
    @abstractmethod
    def resolve_install_requires(self, ctx) -> bool:
        raise NotImplementedError

    @abstractmethod
    def resolve_tests_require(self, ctx) -> bool:
        raise NotImplementedError


class RequirementsTxtRequiresResolver(RequiresResolver):
    def resolve_install_requires(self, ctx) -> bool:
        requirements = ctx.get_text_content('requirements.txt')
        if requirements is None:
            return False

        ctx.setup_attrs['install_requires'] = [l for l in requirements.splitlines() if l]
        return True

    def resolve_tests_require(self, ctx) -> bool:
        return False


class PipfileRequiresResolver(RequiresResolver):
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

    def _pipenv_package_to_require(self, k, v):
        return k

    def _resolve_requires(self, ctx, attr_name, pf_key):
        pf = self._get_pipfile(ctx)
        if pf is None:
            return False
        ctx.setup_attrs[attr_name] = requires = []
        for k, v in pf.data[pf_key].items():
            requires.append(self._pipenv_package_to_require(k, v))
        return True

    def resolve_install_requires(self, ctx) -> bool:
        return self._resolve_requires(ctx, 'install_requires', 'default')

    def resolve_tests_require(self, ctx) -> bool:
        return self._resolve_requires(ctx, 'tests_require', 'develop')


class ChainRequiresResolver(RequiresResolver):
    def __init__(self, *resolvers):
        self.resolvers = list(resolvers)

    def resolve_install_requires(self, ctx) -> bool:
        return any(r.resolve_install_requires(ctx) for r in self.resolvers)

    def resolve_tests_require(self, ctx) -> bool:
        return any(r.resolve_tests_require(ctx) for r in self.resolvers)


class DefaultRequiresResolver(RequiresResolver):
    def __init__(self):
        self._install_resolver = ChainRequiresResolver(
            RequirementsTxtRequiresResolver(),
            PipfileRequiresResolver()
        )
        self._test_resolver = ChainRequiresResolver(
            PipfileRequiresResolver()
        )

    def resolve_install_requires(self, ctx) -> bool:
        return self._install_resolver.resolve_install_requires(ctx)

    def resolve_tests_require(self, ctx) -> bool:
        return self._test_resolver.resolve_tests_require(ctx)
