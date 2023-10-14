import argparse
import sys

from src.algorithm.edmond_blossom import EdmondsBlossom
from src.algorithm.carvalho_cheriyan import CarvalhoCheriyan
from src.common.graph import Graph

parser = argparse.ArgumentParser(description="Animate algorithm with input")
parser.add_argument(
    "algorithm",
    choices=["edmonds", "carvalho_cheriyan"],
    help="Algorithm to be runned"
)
parser.add_argument("test_name", help="Test name")
parser.add_argument(
    "-m", "--manual", dest="manual", action="store_true",
    help="Activates manual mode. You have to do a click in the window in "
    "order to show the next frame of the animation."
)
parser.add_argument(
    "-f", "--frequence", dest="frequence", action="store", type=float,
    default=1000, help="The frequence in miliseconds in which the animation "
    "will be refreshed. The default is 1000."
)
args = parser.parse_args()

sys.stdin = open("tests/" + args.test_name, "r")

algo_map = {
    "edmonds": EdmondsBlossom,
    "carvalho_cheriyan": CarvalhoCheriyan,
}

g = Graph(read=True, animate=True)
algo = algo_map[args.algorithm](g)
algo.animate(args.manual, args.frequence)
