module_hooks
============

An example module hooking system, will be used in PySAMP.

Example:

`python/__init__.py`:

```py
import pysamp.callbacks
from . import vehicles


def OnVehicleDeath(vehicleid: int) -> None:
    print(f'From module "{__name__}": Vehicle {vehicleid} died!')


pysamp.callbacks.hook()
```

`python/vehicles.py`:

```py
def OnVehicleDeath(vehicleid: int) -> None:
    print(f'From module "{__name__}": Vehicle {vehicleid} died!')
```
