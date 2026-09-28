from dataclasses import dataclass
from enum import StrEnum
from typing import Literal, Optional

from xonsh.built_ins import XonshSession  # type: ignore  # noqa: TC002
from xonsh.color_tools import COLORS, find_closest_color, iscolor  # type: ignore noqa: TC002

_COLORS = Literal[
    "BLACK",
    "RED",
    "GREEN",
    "YELLOW",
    "BLUE",
    "PURPLE",
    "CYAN",
    "WHITE",
    "INTENSE_BLACK",
    "INTENSE_RED",
    "INTENSE_GREEN",
    "INTENSE_YELLOW",
    "INTENSE_BLUE",
    "INTENSE_PURPLE",
    "INTENSE_CYAN",
    "INTENSE_WHITE",
]

ANSI_INVERT = "\x1b[7m"
ANSI_CONCEAL = "\x1b[8m"
ANSI_STRIKETHROUGH = "\x1b[9m"
ANSI_RESET = "\x1b[0m"


@dataclass
class HexColor:
    hex: str


ColorSpec = _COLORS | HexColor


@dataclass
class Color:
    name: str
    fg: ColorSpec | None
    bg: ColorSpec | None


class Colorz:
    xsh: XonshSession

    def __init__(self, xsh: XonshSession):
        if xsh is None:
            raise ValueError("XonshSession cannot be None")
        if xsh.env is None:
            raise ValueError("XonshSession.env cannot be None")
        self.xsh = xsh
