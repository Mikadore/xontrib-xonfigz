from dataclasses import dataclass

from xonsh.color_tools import iscolor  # type: ignore  
from xonsh.tools import print_warning

from xontrib_xonfigz.ansi import AnsiSequence


class Color:
    color: str
    
    def __init__(self, color: str):
        if not iscolor(color):
            raise ValueError(f"Invalid color name: {color}")
        self.color = color

    def __str__(self) -> str:
        return self.color

    def __format__(self, format_spec: str) -> str:
        if format_spec:
            raise ValueError(f"Invalid format spec: {format_spec}")
        return self.color

    @staticmethod
    def hex(hex_color: str) -> Color:
        if not hex_color.startswith("#"):
            raise ValueError(f"Invalid hex color: {hex_color}")
        if len(hex_color) != 7 and len(hex_color) != 4:
            raise ValueError(f"Invalid hex color length: {hex_color}")
        return Color(hex_color)

    @staticmethod
    def default() -> Color:
        return Color("DEFAULT")

class ColorNames:
    DEFAULT: Color = Color("DEFAULT")
    BLACK: Color = Color("BLACK")
    RED: Color = Color("RED")
    GREEN: Color = Color("GREEN")
    YELLOW: Color = Color("YELLOW")
    BLUE: Color = Color("BLUE")
    PURPLE: Color = Color("PURPLE")
    CYAN: Color = Color("CYAN")
    WHITE: Color = Color("WHITE")
    INTENSE_BLACK: Color = Color("INTENSE_BLACK")
    INTENSE_RED: Color = Color("INTENSE_RED")
    INTENSE_GREEN: Color = Color("INTENSE_GREEN")
    INTENSE_YELLOW: Color = Color("INTENSE_YELLOW")
    INTENSE_BLUE: Color = Color("INTENSE_BLUE")
    INTENSE_PURPLE: Color = Color("INTENSE_PURPLE")
    INTENSE_CYAN: Color = Color("INTENSE_CYAN")
    INTENSE_WHITE: Color = Color("INTENSE_WHITE")

    def __getattr__(self, name) -> Color:
        color = name.split('_')[-2:]
        if len(color) > 2 or (len(color) == 2 and color[0] != "INTENSE"):
            raise AttributeError(
                f"Invalid color name: {name} (modifiers are forbidden)"
            )
        if iscolor(name):
            return Color(name)
        raise AttributeError(f"Invalid color name: {name}")

    def hex(self, hex_color: str) -> Color:
        return Color.hex(hex_color)


@dataclass
class Style:
    background: Color | None
    foreground: Color | None

    is_bold : bool = False
    """increases font intensity. E.g. BOLD_RED, BOLD_#112233."""

    is_faint : bool = False
    """decreases font intensity. E.g. FAINT_YELLOW."""
 
    is_italic : bool = False
    """switches to italic. E.g. ITALIC_BLUE."""

    is_underline : bool = False
    """adds underline. E.g. UNDERLINE_GREEN."""

    is_invert : bool = False
    """swaps foreground and background. E.g. INVERT_WHITE."""

    is_conceal : bool = False
    """hides text (may not be widely supported). E.g. CONCEAL_BLACK."""

    is_strikethrough : bool = False
    """draws a line through text. E.g. STRIKETHROUGH_RED."""

    is_underline_double : bool = False
    """adds double underline"""

    is_overline : bool = False
    """adds overline"""

    @staticmethod
    def default() -> Style:
        return Style()

    def __init__(
        self,
        background: Color | None = None,
        foreground: Color | None = None,
        bold: bool = False,
        faint: bool = False,
        italic: bool = False,
        underline: bool = False,
        invert: bool = False,
        conceal: bool = False,
        strikethrough: bool = False,
        underline_double: bool = False,
        overline: bool = False,
    ):
        self.background = background
        self.foreground = foreground
        self.is_bold = bold
        self.is_faint = faint
        self.is_italic = italic
        self.is_underline = underline
        self.is_invert = invert
        self.is_conceal = conceal
        self.is_strikethrough = strikethrough
        self.is_underline_double = underline_double
        self.is_overline = overline

    def fg(self, fg: Color) -> Style:
        self.foreground = fg
        return self

    def bg(self, bg: Color) -> Style:
        self.background = bg
        return self

    def bold(self, bold: bool = True) -> Style:
        self.is_bold = bold
        return self

    def faint(self, faint: bool = True) -> Style:
        self.is_faint = faint
        return self

    def italic(self, italic: bool = True) -> Style:
        self.is_italic = italic
        return self

    def underline(self, underline: bool = True, double: bool | None = False) -> Style:
        if underline and double is not None:
            print_warning(
                "Both underline and double underline are set to True. "
                "Double underline will take precedence."
            )
            self.is_underline_double = double
        elif double is not None:
            self.is_underline_double = True
        else:
            self.is_underline = underline
        return self
 
    def invert(self, invert: bool = True) -> Style:
        self.is_invert = invert
        return self

    def conceal(self, conceal: bool = True) -> Style:
        self.is_conceal = conceal
        return self

    def strikethrough(self, strikethrough: bool = True) -> Style:
        self.is_strikethrough = strikethrough
        return self

    def overline(self, overline: bool = True) -> Style:
        self.is_overline = overline
        return self

    def _ansi(self) -> list[AnsiSequence]:
        ansi = []

        if self.is_faint and not self.is_bold:
            ansi.append(AnsiSequence.FAINT)
        elif self.is_bold:
            ansi.append(AnsiSequence.BOLD)

        if self.is_italic:
            ansi.append(AnsiSequence.ITALIC)

        if self.is_underline_double:
            ansi.append(AnsiSequence.DOUBLE_UNDERLINE)
        elif self.is_underline:
            ansi.append(AnsiSequence.UNDERLINE)

        if self.is_overline:
            ansi.append(AnsiSequence.OVERLINE)

        if self.is_invert:
            ansi.append(AnsiSequence.INVERT)
        
        if self.is_conceal:
            ansi.append(AnsiSequence.CONCEAL)

        if self.is_strikethrough:
            ansi.append(AnsiSequence.STRIKETHROUGH)

        return ansi

    def render_modifiers(self) -> str:
        """
        Render the style as a string that can be used in the xonsh prompt.
        """
        return ''.join(map(lambda sq: sq.start(), self._ansi()))

    def render_color(self) -> str:
        style = ""
        if self.foreground is not None:
            style += f"{{{self.foreground}}}"
        else:
            style += f"{{{ColorNames.DEFAULT}}}"
        if self.background is not None:
            style += f"{{BACKGROUND_{self.background}}}"
        else:
            style += f"{{BACKGROUND_{ColorNames.DEFAULT}}}"
        return style
        

    def reset_modifiers(self, keep: list[AnsiSequence] | None = None) -> str:
        """
        Render the style as a string that can be used in the xonsh prompt.
        """
        if keep is None:
            keep = []
        reset_sequences = [sq for sq in self._ansi() if sq not in keep]
        return ''.join(map(lambda sq: sq.end(), reset_sequences))
