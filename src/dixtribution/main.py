"""
Dixipline

"""

import argparse
from itertools import chain
from subprocess import Popen, PIPE
from os import path
import os
import importlib
import asyncio

from .dixtributor import Dixtributor, Msg


# Import dixtributors
dixtributors_path = path.join(path.dirname(__file__), "dixtributors")
all_dixtributors: dict[str, type[Dixtributor]] = {}
for file in os.listdir(dixtributors_path):
    if file.endswith(".py") and file != "__init__.py":
        module = importlib.import_module(
            f".dixtributors.{file.removesuffix('.py')}",
            package="dixtribution")
        for obj_name in dir(module):
            obj = getattr(module, obj_name)
            if (obj != Dixtributor and isinstance(obj, type)
                    and issubclass(obj, Dixtributor)):
                all_dixtributors[obj.CLI_NAME] = obj


def parse_args():
    parser = argparse.ArgumentParser(prog="dixtribution")

    # Dixtribution arguments
    parser.add_argument("-i", "--iterations", type=int, default=10)
    parser.add_argument("-d", "--dixtributors", choices=all_dixtributors.keys(),
                        nargs="+", action="append", required=True,
                        help="Dixtributor to use")

    # Onze arguments
    parser.add_argument("-r", "--rounds", type=int, default=10)
    parser.add_argument("-s", '--seats', nargs="+",
                        action="append", help="Seat")
    return parser.parse_args()


async def play_game(onze_args, dixtributors: list[Dixtributor]):
    proccess = await asyncio.subprocess.create_subprocess_exec(
        "onze", *onze_args, stdout=PIPE)

    assert proccess.stdout is not None
    while (next_msg := await proccess.stdout.readline()):
        msg = Msg.deserialize_msg(next_msg.decode("utf-8"))
        for dixtributor in dixtributors:
            if dixtributor.filter(msg):
                dixtributor.process_msg(msg)


async def main():
    args = parse_args()

    onze_args = ["-r", str(args.rounds)]

    if len(args.seats) != 2:
        args.seats.append(args.seats[0])

    for seat in args.seats:
        onze_args += ["-s", str(seat[0])]

    args.dixtributors = set(chain.from_iterable(args.dixtributors))

    dixtributors = [all_dixtributors[cli_name](args)
                    for cli_name in args.dixtributors]

    # we must play the game sequentially to make the dixtributors consistent
    for _ in range(args.iterations):
        await play_game(onze_args, dixtributors)

    for dixtributor in dixtributors:
        dixtributor.generate_result()


def run():
    asyncio.run(main())
