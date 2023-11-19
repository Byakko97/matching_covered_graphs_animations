import argparse
import sys

from os import listdir

from src.data_structures.graph import Graph
from src.api.utils import algorithm_map

parser = argparse.ArgumentParser(
    description="Test algorithm with all test inputs in tests folder"
)
parser.add_argument(
    "algorithm",
    choices=algorithm_map.keys(),
    help="Algorithm to be tested",
)
args = parser.parse_args()

for test_id in listdir("tests/"):
    sys.stdin = open("tests/" + test_id, "r")
    g = Graph(read=True)

    print(test_id, ": ", end='')

    algo = algorithm_map[args.algorithm](g)
    if algo.test():
        print("OK")
    else:
        print("FAILED")
        break
