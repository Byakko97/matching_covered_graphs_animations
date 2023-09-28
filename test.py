import argparse
import sys

from os import listdir

from src.algorithm.edmond_blossom import EdmondsBlossom
from src.algorithm.carvalho_cheriyan import CarvalhoCheriyan
from src.common.graph import Graph

parser = argparse.ArgumentParser(
    description="Test algorithm with all test inputs in tests folder"
)
parser.add_argument(
    "algorithm",
    choices=["edmonds", "carvalho_cheriyan"],
    help="Algorithm to be tested",
)
args = parser.parse_args()

algo_map = {
    "edmonds": EdmondsBlossom,
    "carvalho_cheriyan": CarvalhoCheriyan,
}

for test_id in listdir("tests/"):
    sys.stdin = open("tests/" + test_id, "r")
    g = Graph(read=True)

    print(test_id, ": ", end='')

    algo = algo_map[args.algorithm](g)
    if algo.test():
        print("OK")
    else:
        print("FAILED")
        break
