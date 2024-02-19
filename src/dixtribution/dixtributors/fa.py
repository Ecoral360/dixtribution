from argparse import Namespace
from ..dixtributor import Dixtributor, Msg, MsgType


def calculate_force(n_iter: int) -> list[float]: ...


class PlotResultDixtributor(Dixtributor):
    def __init__(self, cmd_args: Namespace, dixtributor_args):
        super().__init__(cmd_args, dixtributor_args)
        self.tau = int(dixtributor_args.get("tau", "1"))
        self.n_iter = int(dixtributor_args.get("i", "10"))
        self.n_brasses = cmd_args.rounds

    def filter(self, msg: Msg) -> bool:
        return msg.type in (MsgType.GAME_SCORES, MsgType.FINAL_SCORES)

    def process_msg(self, msg: Msg):
        if msg.type is MsgType.FINAL_SCORES:
            print("new game")
        print(msg.data)

    def generate_result(self):
        pass


__dixtributor__ = PlotResultDixtributor
