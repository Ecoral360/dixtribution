from ..dixtributor import Dixtributor, Msg, MsgType
from argparse import Namespace
from os import path


class ErrDixtributor(Dixtributor):
    def __init__(self, cmd_args: Namespace, dixtributor_args: dict[str, str]):
        super().__init__(cmd_args, dixtributor_args)
        self.invalid_cards = {str(i): [] for i in range(4)}
        self.nb_cards_played = 0
        self.teams = (
            path.basename(cmd_args.seats[0][0]),
            path.basename(cmd_args.seats[1][0]),
        )

        show = list(map(str.strip, dixtributor_args.get("show", "").split(",")))
        self.show_invalid_cards = "cards" in show
        self.show_ratio = "ratio" in show
        self.show_no_err = "ne" in show

    def filter(self, msg: Msg) -> bool:
        return msg.type is MsgType.INVALID_CARD or msg.type is MsgType.CARD_PLAYED

    def process_msg(self, msg: Msg):
        if msg.type is MsgType.CARD_PLAYED:
            self.nb_cards_played += 1
            return

        self.invalid_cards[msg.actor].append(msg.data)

    def generate_result(self):
        for player, cards in self.invalid_cards.items():
            if not cards and not self.show_no_err:
                continue
            team = self.teams[int(player) % 2]
            print(
                f"Player {player}(team {team}) has played {len(cards)} invalid cards "
                f"out of {self.nb_cards_played}:",
            )
            if self.show_ratio:
                print(f"    Ratio: {len(cards) / self.nb_cards_played:.2%}")
                nb_no_card = cards.count("No card")
                print(
                    f"    No card: {nb_no_card}, Wrong card: {len(cards) - nb_no_card}"
                )
            if self.show_invalid_cards:
                print("   ", cards)


__dixtributor__ = ErrDixtributor
