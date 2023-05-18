# Matching Covered Graphs Animations

Animations of algorithms related to matching covered graphs. This project is part of my Bachelor Thesis (under development).

## Usage

The supported functionalities by now are to run and test algorithms (without animation).

### Run algorithms

Use the following command to run the algorithm `algo` with the test `test_id`:

```
python3 run.py algo test_id
```

The tests are in the folder `tests` and the id of a test is the name of the file in which it is contained.

### Test algorithms

Use the following command to test the algorithm `algo` with all the tests in the folder `tests`:

```
python3 test.py algo
```

### Supported algorithms

The currently supported algorithms are:

* `edmonds`: Edmonds's Blossom algorithm