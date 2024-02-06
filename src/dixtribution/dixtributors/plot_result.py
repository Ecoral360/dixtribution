from ..dixtributor import Dixtributor, Msg


class PlotResultDixtributor(Dixtributor):
    CLI_NAME = "plt_res"

    def filter(self, msg: Msg) -> bool:
        ...

    def process_msg(self, msg: Msg):
        ...

    def generate_result(self):
        ...
