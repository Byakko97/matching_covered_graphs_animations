import argparse
import sys

from src.algorithm.edmond_blossom import EdmondsBlossom
from src.common.graph import Graph

parser = argparse.ArgumentParser(description="Test algorithm with all test inputs in tests folder")
parser.add_argument("algorithm", choices=["edmonds"], help="Algorithm to be tested")
args = parser.parse_args()

#TODO: get the actual range
for test_id in range(1, 11):
    sys.stdin = open("tests/" + str(test_id), "r")

    g = Graph()
    g.read()

    algo = EdmondsBlossom(g)
    if algo.verify():
        print("OK")
    else:
        print("FAILED ON TEST " + str(test_id))
        break