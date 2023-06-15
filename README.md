# Matching Covered Graphs Animations

Animations of algorithms related to matching covered graphs. This project is part of my Bachelor Thesis (under development).

## Usage

The supported functionalities are to run and test algorithms.

### Run algorithms

Use the following command to run the algorithm `algo` with the test `test_id`:

```
python3 run.py algo test_id
```

The tests are in the folder `tests` and the id of a test is the name of the file in which it is contained.

Add the flag `-a` if you want to see an animation of the algorithm.

```
python3 run.py algo test_id -a
```
### Test algorithms

Use the following command to test the algorithm `algo` with all the tests in the folder `tests`:

```
python3 test.py algo
```

### Supported algorithms

The currently supported algorithms are:

* `edmonds`: Edmonds's Blossom algorithm