import sys
import warnings
from importlib.machinery import SOURCE_SUFFIXES, FileFinder, SourceFileLoader
from types import ModuleType

from .callbacks import callback_registry, hook_callbacks


__all__ = ('hook_callbacks',)


class PySAMPImportWarning(RuntimeWarning):
    """Gets issued if it seems like import order is incorrect."""
    pass


class PySAMPLoader(SourceFileLoader):
    """Custom loader that registers module callbacks on import."""
    def exec_module(self, module: ModuleType) -> None:
        super().exec_module(module)

        if not self.name.startswith('python.'):
            return

        callback_registry.register_module(module)


for module_name in sys.modules:
    if module_name.startswith('python.'):
        warnings.warn(
            f'Module {module_name} was imported before pysamp, '
            'this is probably not what you want.',
            category=PySAMPImportWarning,
        )

sys.path_hooks.insert(
    0,
    # See typeshed issues #7085 and #7086
    FileFinder.path_hook((PySAMPLoader, SOURCE_SUFFIXES))  # type: ignore
)
