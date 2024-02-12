from ..dixtributor import Dixtributor, Msg, MsgType
from os import path
import matplotlib.pyplot as plt


class PlotResultDixtributor(Dixtributor):
    def __init__(self, cmd_args, *dixtributor_args):
        super().__init__(cmd_args, *dixtributor_args)
        self.teams = (path.basename(cmd_args.seats[0][0]),
                      path.basename(cmd_args.seats[1][0]))
        self.results = []

    def filter(self, msg: Msg) -> bool:
        return msg.type is MsgType.FINAL_SCORES

    def process_msg(self, msg: Msg):
        self.results.append(msg.data)

    def generate_result(self):
        for i, team in enumerate(self.teams):
            plt.plot([result[str(i)]
                     for result in self.results], label=f"Team {team}")
        plt.legend()
        plt.show()


__dixtributor__ = PlotResultDixtributor
