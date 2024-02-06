"""
Dixipline

"""

import argparse
from subprocess import Popen, PIPE
import matplotlib.pyplot as plt
from os import path
import os
import importlib

from .dixtributor import Dixtributor


# Import dixtributors
dixtributors_path = path.join(path.dirname(__file__), "dixtributors")
dixtributors = {}
for file in os.listdir(dixtributors_path):
    if file.endswith(".py") and file != "__init__.py":
        module = importlib.import_module(
            f".dixtributors.{file.removesuffix('.py')}",
            package="dixtribution")
        for obj_name in dir(module):
            obj = getattr(module, obj_name)
            if (obj != Dixtributor and isinstance(obj, type)
                    and issubclass(obj, Dixtributor)):
                dixtributors[obj.CLI_NAME] = obj


def parse_args():
    parser = argparse.ArgumentParser(prog="dixtribution")

    # Dixtribution arguments
    parser.add_argument("-i", "--iterations", type=int, default=10)
    parser.add_argument("-d", "--dixtributor", choices=dixtributors.keys(),
                        nargs="+", action="append",
                        default=None, help="Dixtributor to use")

    # Onze arguments
    parser.add_argument("-r", "--rounds", type=int, default=10)
    parser.add_argument("-s", '--seats', nargs="+",
                        action="append", help="Seat")
    return parser.parse_args()


def play_game(onze_args) -> dict:
    proccess = Popen(onze_args, stdout=PIPE, text=True, encoding="utf-8")
    output, _ = proccess.communicate()
    result = output.split("\n")[-2].removeprefix("[server] total_scores=")
    print(result)
    return eval(result)


def plot_game_results(teams: tuple[str, str], results: list[dict]):
    for i, team in enumerate(teams):
        plt.plot([result[i] for result in results], label=f"Team {team}")
    plt.legend()
    plt.show()


def run():
    args = parse_args()

    onze_args = ["onze", "-r", str(args.rounds)]

    if len(args.seats) != 2:
        args.seats.append(args.seats[0])

    teams = (path.basename(args.seats[0][0]),
             path.basename(args.seats[1][0]))

    for seat in args.seats:
        onze_args += ["-s", str(seat[0])]

    results = [play_game(onze_args) for _ in range(args.iterations)]

    plot_game_results(teams, results)
