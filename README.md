# firstRoboPy
A very simple first attempt at robot written in python

![Workflow Status](https://github.com/RobotCasserole1736/firstRoboPy/actions/workflows/ci.yml/badge.svg)

## Installation

Before developing code on a new computer, perform the following:

1. [Download and install wpilib](https://github.com/wpilibsuite/allwpilib/releases)
2. [Download and install python](https://www.python.org/downloads/)
3. Run these commands:

```cmd
    cd TO_THE_DIRECTORY_THAT_WAS_CLONED
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
```

```cmd
python -m robotpy_installer download-python
python -m robotpy_installer download -r roborio_requirements.txt
```

7. Power-up the robot
5. Make sure that you're on the same network as the robot
5.1 One way is to leave your computer connected to WiFi internet and make a wired Ethernet connection to the robot
5.2 Another way is to connect your computer to the robot over WiFi
6. Optionally reflash your roboRIO like this to get a clean install: https://docs.wpilib.org/en/stable/docs/zero-to-robot/step-3/index.html
7. Install needed python and libraries on the RoboRIO see: https://robotpy.readthedocs.io/en/stable/install/robot.html#install-robotpy

```cmd
python -m robotpy_installer install-python
python -m robotpy_installer install robotpy
python -m robotpy_installer install debugpy
python -m robotpy_installer install robotpy[ctre]
python -m robotpy_installer install robotpy[rev]
python -m robotpy_installer install robotpy[navx]
python -m robotpy_installer install robotpy[pathplannerlib]
```

## Docs

[Click here to see documentation for common libraries](docs/UserAPI).

## The robot website

On a simulator: http://localhost:5805/

On a RoboRIO:

* RobotCasserole: http://10.17.36.2:5805/
* Spires: http://10.91.6.2:5805/

# TODO Fix these up.

## Deploying to the Robot

`deploy.bat` will deploy all code to the robot. Be sure to be on the same network as the robot.

`.deploy_cfg` contains specific configuration about the deploy process.

## Linting

"Linting" is the process of checking our code format and style to keep it looking nice

`lint.bat` will execute the linter.

`.pylintrc` contains configuration about what checks the linter runs, and what formatting it enforces

## Testing

Run the `Test` configuration in the debugger in vsCode.

## Simulating

Run the `Simulate` configuration in the debugger in vsCode.

## Continuous Integration

Github runs our code on its servers on every commit to ensure our code stays high quality. This is called "Continuous Integration".

`.github/workflows/ci.yml` contains configuration for all the commands that our continuous integration environment.

To minimize frustration and rework, before committing, be sure to:

1. Run the test suite
2. Run `lint.bat` and fix any formatting errors
