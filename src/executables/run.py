import argparse
import sys

from src.algorithm.edmond_blossom import EdmondsBlossom
from src.algorithm.carvalho_cheriyan import CarvalhoCheriyan
from src.common.graph import Graph

parser = argparse.ArgumentParser(description="Run algorithm with input")
parser.add_argument(
    "algorithm",
    choices=["edmonds", "carvalho_cheriyan"],
    help="Algorithm to be runned"
)
parser.add_argument("test_name", help="Test name")
args = parser.parse_args()

sys.stdin = open("tests/" + args.test_name, "r")

algo_map = {
    "edmonds": EdmondsBlossom,
    "carvalho_cheriyan": CarvalhoCheriyan,
}

g = Graph(read=True)
algo = algo_map[args.algorithm](g)
algo.run()
