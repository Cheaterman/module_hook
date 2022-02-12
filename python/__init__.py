import pysamp
from . import vehicles


def OnVehicleDeath(vehicleid: int) -> None:
    print(f'From module "{__name__}": Vehicle {vehicleid} died!')


pysamp.hook_callbacks()
