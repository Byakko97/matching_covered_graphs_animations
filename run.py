import argparse
import sys

from src.algorithm.edmond_blossom import EdmondsBlossom
from src.common.graph import Graph

parser = argparse.ArgumentParser(description="Run algorithm with input")
parser.add_argument("algorithm", choices=["edmonds"], help="Algorithm to be runned")
parser.add_argument("test_id", help="Test id")
parser.add_argument("-a", "--animate", dest="animate", action="store_true", help="Animate the algorithm")
args = parser.parse_args()

sys.stdin = open("tests/" + args.test_id, "r")

g = Graph(read=True, animate=args.animate)

algo = EdmondsBlossom(g)

if args.animate:
    algo.animate()
else:
    algo.run()