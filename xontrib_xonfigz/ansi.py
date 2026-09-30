from enum import Enum

# | Effect | Enable | Disable |
# |---|---:|---:|
# | Reset everything | `0` | — |
# | Bold | `1` | `22` |
# | Faint/dim | `2` | `22` |
# | Italic | `3` | `23` |
# | Underline | `4` | `24` |
# | Invert/reverse | `7` | `27` |
# | Conceal/hidden | `8` | `28` |
# | Strikethrough | `9` | `29` |
# | Double underline | `21` | `24` |
# | Overline | `53` | `55` |

_ANSI = "\x1b["

class AnsiSequence(Enum):
    RESET = "RESET"
    BOLD = "BOLD"
    FAINT = "FAINT"
    ITALIC = "ITALIC"
    UNDERLINE = "UNDERLINE"
    INVERT = "INVERT"
    CONCEAL = "CONCEAL"
    STRIKETHROUGH = "STRIKETHROUGH"
    DOUBLE_UNDERLINE = "DOUBLE_UNDERLINE"
    OVERLINE = "OVERLINE"

    def reset(self) -> str:
        return _ANSI + "0m"

    def start(self) -> str:
        match self:
            case AnsiSequence.BOLD:
                return _ANSI + "1m"
            case AnsiSequence.FAINT:
                return _ANSI + "2m"
            case AnsiSequence.ITALIC:
                return _ANSI + "3m"
            case AnsiSequence.UNDERLINE:
                return _ANSI + "4m"
            case AnsiSequence.INVERT:
                return _ANSI + "7m"
            case AnsiSequence.CONCEAL:
                return _ANSI + "8m"
            case AnsiSequence.STRIKETHROUGH:
                return _ANSI + "9m"
            case AnsiSequence.DOUBLE_UNDERLINE:
                return _ANSI + "21m"
            case AnsiSequence.OVERLINE:
                return _ANSI + "53m"
            case _:
                raise ValueError(f"Unknown AnsiSequence: {self}")

    def end(self) -> str:
        match self:
            case AnsiSequence.BOLD:
                return _ANSI + "22m"
            case AnsiSequence.FAINT:
                return _ANSI + "22m"
            case AnsiSequence.ITALIC:
                return _ANSI + "23m"
            case AnsiSequence.UNDERLINE:
                return _ANSI + "24m"
            case AnsiSequence.INVERT:
                return _ANSI + "27m"
            case AnsiSequence.CONCEAL:
                return _ANSI + "28m"
            case AnsiSequence.STRIKETHROUGH:
                return _ANSI + "29m"
            case AnsiSequence.DOUBLE_UNDERLINE:
                return _ANSI + "24m"
            case AnsiSequence.OVERLINE:
                return _ANSI + "55m"
            case _:
                raise ValueError(f"Unknown AnsiSequence: {self}")
