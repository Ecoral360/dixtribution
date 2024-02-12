from abc import ABC, abstractmethod
from argparse import Namespace
from typing import Literal
from enum import Enum
import json
from dataclasses import dataclass


class MsgType(Enum):
    SEED = "seed"

    INVALID_CARD = "invalid-card"
    CARD_PLAYED = "card-played"
    PLAYER_START_HAND = "player-start-hand"
    PLAYER_PLAYABLE_HAND = "player-playable-hand"
    PLAYER_BID = "player-bid"
    PLAYER_SEAT = "player-seat"

    SEAT_DEBUG_MSG = "seat-debug-msg"

    GAME_SCORES = "game-scores"
    TOTAL_SCORES = "total-scores"
    FINAL_SCORES = "final-scores"


@dataclass
class Msg:
    actor: (Literal["0"]
            | Literal["1"]
            | Literal["2"]
            | Literal["3"]
            | Literal["server"])
    type: MsgType
    data: dict | str | int | float

    @staticmethod
    def deserialize_msg(msg: str) -> "Msg":
        msg_json = json.loads(msg)
        return Msg(actor=msg_json["actor"],
                   type=MsgType(msg_json["type"]),
                   data=msg_json["data"])


class Dixtributor(ABC):
    def __init__(self, cmd_args: Namespace, *dixtributor_args):
        self.cmd_args = cmd_args
        self.dixtributor_args = dixtributor_args

    @abstractmethod
    def filter(self, msg: Msg) -> bool:
        """
        If the Dixtributor wants to act on this message, return True
        """
        ...

    @abstractmethod
    def process_msg(self, msg: Msg):
        ...

    @abstractmethod
    def generate_result(self):
        """
        Called at the end of the game to generate the result
        """
        ...
