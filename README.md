# Matching Covered Graphs Animations

Animations of algorithms related to matching covered graphs. This project is part of my Bachelor Thesis (under development).

## Requirements

In order to use this program, you must install `graph-tools`. Follow the [official installation instructions](https://git.skewed.de/count0/graph-tool/-/wikis/installation-instructions) to do so.

## Usage

The supported functionalities are to animate, run and test algorithms.

### Animate 

Use the following command to animate the algorithm `algo` with the input test `test_name`:

```
python3 animate.py algo test_name
```

The tests are in the folder `tests`. The name of a test is the name of the tile that contains it.

If you want to adjust the speed of the animation, use the flag `--frequence` (`-f` for abbreviation) followed by the frequence, in miliseconds, in which the animation will be refreshed. The default refresh frequence is 1000 miliseconds. For example if you want to see the animation two times faster than the default speed, do

```
python3 animate.py algo test_name -f 500
```

If you rather execute the animation manually, you can do it using the flag `-m`. In that case, you will have to do a click in the animation window everytime you want to execute the next step of the animation.

```
python3 animate.py algo test_name -m
```

### Run algorithms

If you just want to run the algorithm `algo` with the input test `test_name` without animation, execute the following command:

```
python3 run.py algo test_name
```

### Test algorithms

Use the following command to test the algorithm `algo` with all the tests in the folder `tests`:

```
python3 test.py algo
```

### Supported algorithms

The currently supported algorithms are:

* `edmonds`: Edmonds's Blossom algorithm