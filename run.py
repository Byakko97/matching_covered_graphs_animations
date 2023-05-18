import argparse
import sys

from src.algorithm.edmond_blossom import EdmondsBlossom
from src.common.graph import Graph

parser = argparse.ArgumentParser(description="Run algorithm with input")
parser.add_argument("algorithm", choices=["edmonds"], help="Algorithm to be runned")
parser.add_argument("test_id", help="Test id")
args = parser.parse_args()

sys.stdin = open("tests/" + args.test_id, "r")

g = Graph()
g.read()

algo = EdmondsBlossom(g)
algo.run()