import wpilib
from json import load as load

robotConfig = {}
try:
    with open(f"{wpilib.getDeployDirectory()}/robotConfig.json") as file:
        robotConfig = load(file)
except:
    robotConfig = {"teamnumber": 1736, "year": 2024, "robotname": "casseroleOne"}

print(f"robotConfig.robotConfig={robotConfig}")


def isCasserole():
    return 1736==robotConfig['teamnumber']

def isSpires2024Tomahawk():
    return 9106==robotConfig['teamnumber'] and 'tomahawk'==robotConfig['robotname']