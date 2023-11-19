import argparse
import sys

from src.data_structures.graph import Graph
from src.api.utils import algorithm_map

parser = argparse.ArgumentParser(description="Animate algorithm with input")
parser.add_argument(
    "algorithm",
    choices=algorithm_map.keys(),
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

g = Graph(read=True, animate=True)
algo = algorithm_map[args.algorithm](g)
algo.animate(args.manual, args.frequence)
