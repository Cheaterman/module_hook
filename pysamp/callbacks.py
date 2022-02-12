from collections import defaultdict
from dataclasses import dataclass, field
from types import ModuleType
from typing import Any, Callable, Dict, List, Optional, Tuple


callback_names = (
    'OnVehicleDeath',
)


@dataclass
class HookedCallback:
    """A hooked callback. Assigned to python module on pysamp import.

    Calls main callback in "python" module, then registered module callbacks.
    """
    name: str
    main_callback: Optional[Callable[..., None]]

    def __call__(self, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> None:
        """Call the real callback first, then all registered modules'."""
        if(
            self.main_callback
            and self.main_callback(*args, **kwargs) is False
        ):
            return

        callback_registry.dispatch(self.name, *args, **kwargs)


@dataclass
class CallbackRegistry:
    """A registry for module callbacks. Gets populated on pysamp import."""
    _by_module_name: Dict[str, List[Callable[..., None]]] = field(
        default_factory=lambda: defaultdict(list)
    )
    _by_callback_name: Dict[str, List[Callable[..., None]]] = field(
        default_factory=lambda: defaultdict(list)
    )

    def register_module(self, module: ModuleType) -> None:
        """Register all callbacks in a module, called on import."""
        for name in callback_names:
            callback = getattr(module, name, None)

            if not callback:
                continue

            self.register_callback(callback, name, module.__name__)

    def register_callback(
        self,
        callback: Callable[..., None],
        name: str,
        module_name: Optional[str] = None,
    ) -> None:
        """Register callback, called by register_module for each callback."""
        self._by_callback_name[name].append(callback)

        if module_name:
            self._by_module_name[module_name].append(callback)

    def dispatch(
        self,
        callback_name: str,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any]
    ) -> None:
        """Dispatch an event to all registered module callbacks."""
        for callback in self._by_callback_name[callback_name]:
            if callback(*args, **kwargs) is False:
                break


def hook_callback(module: ModuleType, name: str) -> None:
    """Hooks a single callback from given module.

    Makes top level callbacks in the module use callbacks registry.
    """
    main_callback = getattr(module, name, None)
    setattr(module, name, HookedCallback(name, main_callback))


def hook_callbacks() -> None:
    """Hooks all callbacks from user's "python" module.

    Hooks are later used to call registered callbacks inside submodules.
    """
    import python

    for name in callback_names:
        hook_callback(python, name)


callback_registry = CallbackRegistry()
