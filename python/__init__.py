import pysamp.callbacks
from . import vehicles  # noqa


def OnVehicleDeath(vehicleid: int) -> None:
    print(f'From module "{__name__}": Vehicle {vehicleid} died!')


pysamp.callbacks.hook()
