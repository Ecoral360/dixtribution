"""
Dixipline

"""

import argparse
from subprocess import Popen, PIPE
import matplotlib.pyplot as plt
from os import path


def parse_args():
    parser = argparse.ArgumentParser(description="Alice")
    parser.add_argument("-i", "--iterations", type=int, default=10)
    parser.add_argument("-r", "--rounds", type=int, default=10)
    parser.add_argument("-s", '--seat', nargs="+",
                        action="append", help="Seat")
    parser.add_argument("-t", "--teams", nargs="+",
                        action="append", default=None)
    return parser.parse_args()


def play_game(onze_args) -> dict:
    proccess = Popen(onze_args, stdout=PIPE, text=True, encoding="utf-8")
    output, _ = proccess.communicate()
    result = output.split("\n")[-2].removeprefix("[server] total_scores=")
    print(result)
    return eval(result)


def plot_game_results(teams: tuple[str, str], results: list[dict]):
    plt.plot([result[0] for result in results], label=f"Team {teams[0]}")
    plt.plot([result[1] for result in results], label=f"Team {teams[1]}")
    plt.legend()
    plt.show()


def run():
    args = parse_args()

    onze_args = ["onze", "-r", str(args.rounds)]

    teams = args.teams
    if teams is None:
        teams = (path.basename(args.seat[0][0]),
                 path.basename(args.seat[1][0]))

    for seat in args.seat:
        onze_args += ["-s", str(seat[0])]

    results = [play_game(onze_args) for _ in range(args.iterations)]

    plot_game_results(teams, results)
