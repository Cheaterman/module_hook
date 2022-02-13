import python
from pysamp.callbacks import registry


def kill_vehicle(vehicleid: int) -> None:
    python.OnVehicleDeath(vehicleid)


if __name__ == '__main__':
    # Some test code
    kill_vehicle(123)
    registry.unregister('python.vehicles')
    kill_vehicle(124)
