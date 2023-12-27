# firstRoboPy
A very simple first attempt at robot written in python

![Workflow Status](https://github.com/RobotCasserole1736/firstRoboPy/actions/workflows/ci.yml/badge.svg)

## Installation

Before developing code on a new computer, perform the following:

1. [Download and install wpilib](https://github.com/wpilibsuite/allwpilib/releases)
2. [Download and install python](https://www.python.org/downloads/)
3. Run these commands:

```cmd
    python -m pip install --upgrade pip
    python -m pip install robotpy[all]
    python -m pip install -r requirements_dev.txt
    python -m pip install -r requirements_run.txt
```

## Docs

[Click here to see documentation for common libraries](docs/UserAPI).

## The robot website

On a simulator: http://localhost:5805/

On a RoboRIO:

* RobotCasserole: http://10.17.36.2:5805/
* Spires: http://10.91.6.2:5805/

# Interesting commands

## options for pytest


Add a space '--' space and then pytest options: https://docs.pytest.org/en/6.2.x/usage.html

```cmd
python .\robot.py test -- -xvv
python .\robot.py test -- -xvvvv
python .\robot.py test -- -xlsvvvv
```

`-xvv` is the same as `-x -vv`

`-xlsvvvv` is the same as `-x -l -s -vvvv`
```

Details

```cmd
python .\robot.py test -- --tb=auto    # (default) 'long' tracebacks for the first and last
                                       # entry, but 'short' style for the other entries
python .\robot.py test -- --tb=long    # exhaustive, informative traceback formatting
python .\robot.py test -- --full-trace # long traces to be printed on error (longer than --tb=long). It also ensures 
                                       # that a stack trace is printed on KeyboardInterrupt (Ctrl+C). This is very 
                                       # useful if the tests are taking too long and you interrupt them with Ctrl+C to 
                                       # find out where the tests are hanging. By default no output will be shown 
                                       # (because KeyboardInterrupt is caught by pytest). By using this option you make
                                       # sure a trace is shown.
python .\robot.py test -- -l           # pytest lets the stderr/stdout flow through to the console
python .\robot.py test -- -s           # pytest lets the stderr/stdout flow through to the console
python .\robot.py test -- -v           # show each individual test step
python .\robot.py test -- -vv          # pytest shows more details of what faild
python .\robot.py test -- -vvv         # some plugins might make use of -vvv verbosity.
python .\robot.py test -- -vvvv        # some plugins might make use of -vvvv verbosity.
python .\robot.py test -- -x           # stop after first failure
```

# Interesting links

https://github.com/robotpy/mostrobotpy

https://docs.pytest.org/en/7.4.x/

https://pytest.org/en/7.4.x/example/index.html


# TODO Fix these up.

## Deploying to the Robot

`deploy.bat` will deploy all code to the robot. Be sure to be on the same network as the robot.

`.deploy_cfg` contains specific configuration about the deploy process.

Note any folder or file prefixed with a `.` will be skipped in the deploy.

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

## RIO First-time Installation

Follow [the robotpy instructions for setting up the RIO](https://robotpy.readthedocs.io/en/stable/install/robot.html)

Then, install all packages specific to our repo, from `requirements.txt`, following the [two step process for roboRIO package installer](https://robotpy.readthedocs.io/en/stable/install/packages.html)

While on the internet:

`python -m robotpy_installer download -r requirements_run.txt`

Then, while connected to the robot's network:

`python -m robotpy_installer install -r requirements_run.txt`

## Dependency Management

In python, `requirements.txt` lists out all the non-standard packages that need to be installed.

However, a few hangups:

* The list of dependencies for the RIO and for our PC's to do software development is different
* The RIO has limited disk storage space, so we don't want extra packages if we can avoid it.

For now, we're resolving that by having two requirements files - `requirements_dev.txt` lists everything needed just for software development. `requirements_run.txt` lists everything needed to run the code.

Development PC's should pip-install both.

The RoboRIO should only install _run.txt

When recording a new dependency, run `pip freeze > tmp.txt`, then open up `tmp.txt`. It will have a lot of things inside it. Find your new dependency in the list, and add it to the appropriate requirements file. Then delete `tmp.txt`
