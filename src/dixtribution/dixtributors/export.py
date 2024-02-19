from ..dixtributor import Dixtributor, Msg, MsgType
from os import path
import json
import csv


def valid_fmt_or_raise(fmt: str) -> str:
    if fmt not in ["json", "csv"]:
        raise ValueError(f"Invalid format {fmt}")
    return fmt


class ExportDixtributor(Dixtributor):
    def __init__(self, cmd_args, dixtributor_args):
        super().__init__(cmd_args, dixtributor_args)
        self.teams = (
            path.basename(cmd_args.seats[0][0]),
            path.basename(cmd_args.seats[1][0]),
        )

        self.export_file = "results"
        self.export_fmt = "json"

        if (file := dixtributor_args.get("o")) is not None:
            self.export_file = file.split(".")[0]
            if "." in file:
                self.export_fmt = valid_fmt_or_raise(file.split(".")[-1])
        if (fmt := dixtributor_args.get("fmt")) is not None:
            self.export_fmt = valid_fmt_or_raise(fmt)

        self.data = []

    def filter(self, msg: Msg) -> bool:
        return msg.type is MsgType.FINAL_SCORES

    def process_msg(self, msg: Msg):
        self.data.append(msg.data)

    def generate_result(self):
        match self.export_fmt:
            case "json":
                with open(f"{self.export_file}.json", "w") as f:
                    f.write(json.dumps(self.data))
            case "csv":
                with open(f"{self.export_file}.csv", "w") as f:
                    writer = csv.writer(f)
                    writer.writerow(self.teams)
                    for row in self.data:
                        writer.writerow(row.values())


__dixtributor__ = ExportDixtributor
