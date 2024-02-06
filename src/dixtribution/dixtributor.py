from abc import ABC, abstractmethod
from typing import Literal, TypedDict
from enum import Enum


class MsgType(Enum):
    SEED = "seed"
    INVALID_CARD = "invalid-card"
    CARD_PLAYED = "card-played"
    TOTAL_SCORES = "total-scores"


class Msg(TypedDict):
    actor: (Literal["0"]
            | Literal["1"]
            | Literal["2"]
            | Literal["3"]
            | Literal["server"])
    result: MsgType
    data: dict | str | int | float


class Dixtributor(ABC):
    CLI_NAME: str

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, "CLI_NAME"):
            raise AttributeError("Subclass must have a CLI_NAME attribute")

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
