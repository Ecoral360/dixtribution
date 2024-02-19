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
            f".dixtributors.{file.removesuffix('.py')}", package="dixtribution"
        )
        if not hasattr(module, "__dixtributor__"):
            raise ImportError(
                f"Module {file.removesuffix('.py')} does not contain a __dixtributor__"
            )
        all_dixtributors[file.removesuffix(".py")] = getattr(module, "__dixtributor__")


class DixtributorAction(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super().__init__(option_strings, dest, nargs=nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        assert values is not None

        if values[0] not in all_dixtributors:
            parser.error(
                "Invalid dixtributor, must be one of the following: "
                f"{{{', '.join(all_dixtributors.keys())}}}"
            )

        total_values = getattr(namespace, self.dest, []) or []
        total_values.append([values[0], *values[1:]])
        setattr(namespace, self.dest, total_values)


def parse_args():
    parser = argparse.ArgumentParser(prog="dixtribution")

    parser.add_argument("-V", "--version", action="version", version="%(prog)s 0.1")

    # Dixtribution arguments
    parser.add_argument("-i", "--iterations", type=int, default=10)
    parser.add_argument(
        "-d",
        "--dixtributors",
        nargs="+",
        action=DixtributorAction,
        help="Dixtributor to use",
        metavar=(f"{{{', '.join(all_dixtributors)}}}", "args"),
    )

    # Onze arguments
    parser.add_argument("-r", "--rounds", type=int, default=10)
    parser.add_argument("-s", "--seats", nargs="+", action="append", help="Seat")
    parser.add_argument(
        "-c", "--config", type=argparse.FileType("r"), help="Config file"
    )
    return parser.parse_args()


async def play_game(onze_args, dixtributors: list[Dixtributor]):
    proccess = await asyncio.subprocess.create_subprocess_exec(
        "onze", *onze_args, stdout=PIPE
    )

    assert proccess.stdout is not None
    while next_msg := await proccess.stdout.readline():
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

    dixtributors = [
        all_dixtributors[dixtributor_name](
            args,
            {
                key: value[0] if value else key
                for key, *value in map(lambda arg: arg.split("=", 1), rest)
            },
        )
        for [dixtributor_name, *rest] in args.dixtributors
    ]

    # we must play the game sequentially to make the dixtributors consistent
    for _ in range(args.iterations):
        await play_game(onze_args, dixtributors)

    for dixtributor in dixtributors:
        dixtributor.generate_result()


def run():
    asyncio.run(main())
