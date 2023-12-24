# Matching Covered Graphs Animations

Animations of algorithms related to matching covered graphs. This project is part of my Bachelor Thesis (under development).

## Setup

In order to use this program, you must install `graph-tools`. Follow the [official installation instructions](https://git.skewed.de/count0/graph-tool/-/wikis/installation-instructions) to do so.

Then, run 

```
python3 -m pip install -e .
```

to install this project.

## Usage

### Supported algorithms

The currently supported algorithms are:

* `edmonds`: Edmonds's Blossom algorithm
* `carvalho_cheriyan`: Carvalho-Cheriyan algorithm to decide if a graph is matching covered


### Animate 

Use the following command to animate the algorithm `algo_name` with the input test `test_name`:

```
make animate algo=algo_name test=test_name
```

The tests are in the folder `tests`. The name of a test is the name of the file that contains it.

If you want to adjust the speed of the animation,  `f=frequence`, where `frequence` is frequence, in miliseconds, in which the animation will be refreshed. The default refresh frequence is 1000 miliseconds. For example if you want to see the animation two times faster than the default speed, do

```
make animate algo=algo_name test=test_name f=500
```

If you rather execute the animation manually, you can do it adding `m=true`. In that case, you will have to do a click in the animation window everytime you want to execute the next step of the animation.

```
make animate algo=algo_name test=test_name m=true
```

You can also execute the animation offscreen. In that case, the animation frames will be saved in the folder `frames`. To execute the animation in this mode, run

```
make animate algo=algo_name test=test_name off=true

```

### Run algorithms

If you just want to run the algorithm `algo_name` with the input test `test_name` without animation, execute the following command:

```
make run algo=algo_name test=test_name
```

### Test algorithms

Use the following command to test the algorithm `algo_name` with all the tests in the folder `tests`:

```
make test algo=algo_name
```
