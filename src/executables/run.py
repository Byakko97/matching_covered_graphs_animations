import argparse
import sys

from src.common.graph import Graph
from src.executables.utils import algorithm_map

parser = argparse.ArgumentParser(description="Run algorithm with input")
parser.add_argument(
    "algorithm",
    choices=algorithm_map.keys(),
    help="Algorithm to be runned"
)
parser.add_argument("test_name", help="Test name")
args = parser.parse_args()

sys.stdin = open("tests/" + args.test_name, "r")

g = Graph(read=True)
algo = algorithm_map[args.algorithm](g)
algo.run()
