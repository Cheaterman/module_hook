import python
import pysamp  # noqa: unused


def kill_vehicle(vehicleid):
    # Call the callback in main module, it's hooked by now
    python.OnVehicleDeath(vehicleid)


if __name__ == '__main__':
    # Some test code
    import json  # noqa: Test to see if json gets hooked (it shouldn't)
    kill_vehicle(123)
