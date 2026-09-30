import os
import pwd
import shutil
from typing import ClassVar, Self
from pathlib import Path

from xonsh.built_ins import XonshSession  # type: ignore  # noqa: TC002
from xonsh.tools import print_warning, expand_path  # type: ignore

from xontrib_xonfigz.color import ColorNames, Style
from xontrib_xonfigz.prompt import PromptBuilder


class Xonfigz:
    xsh: XonshSession
    style_map: dict[str, Style]
    _instance: ClassVar[Self | None] = None

    def __init__(self, xsh: XonshSession):
        if xsh is None:
            raise ValueError("XonshSession cannot be None")
        if xsh.env is None:
            raise ValueError("XonshSession.env cannot be None")
        self.style_map = {}
        self.xsh = xsh
        pw = pwd.getpwuid(os.getuid())
        if 'USER' not in self.ENV:
            self.env("USER", pw.pw_name)
        else:
            if pw.pw_name != str(self.env("USER")):
                raise RuntimeError(
                    f"Current user {pw.pw_name} does not match"
                    f"XonshSession user {self.env('USER')}"
                )
        

    @classmethod
    def initialize(cls, xsh: XonshSession) -> Xonfigz: # type: ignore
        if cls._instance is None:
            cls._instance = cls(xsh) # type: ignore
        elif cls._instance.xsh is not xsh:
            raise RuntimeError("Xonfigz is already bound to another Xonsh session")
        return cls._instance # type: ignore

    @classmethod
    def instance(cls) -> Self:
        if cls._instance is None:
            raise RuntimeError(
                "Xonfigz has not been initialized; load the xontrib first"
            )
        return cls._instance
    
    def home(self, path: str | None = None) -> str:
        """
        Get the home directory of the current user.
        If path is provided, it will be joined to the home directory.
        """
        if path is None:
            return str(self.xsh.env["HOME"])  # type: ignore
        else:
            self.env("HOME", path)
        return str(self.xsh.env["HOME"])  # type: ignore

    def path(self, entries: str | Path | list[str | Path]) -> list[str]:
        """
        Appends one or more paths to the PATH environment variable
        """
        if isinstance(entries, (str, Path)):
            entries = [entries]
        elif not isinstance(entries, list):
            raise TypeError("entries must be a string, Path, or list of strings/Paths")
        current_path = self.xsh.env.get("PATH", [])  # type: ignore
        new_entries = [str(entry) for entry in entries]
        for entry in new_entries:
            if entry not in current_path:
                p = Path(expand_path(str(entry)))
                if p.exists() and p.is_dir():
                    current_path.append(str(entry))
                else:
                    if not p.exists():
                        print_warning(f"Path does not exist: {entry}")
                    elif not p.is_dir():
                        print_warning(f"Path is not a directory: {entry}")

        self.xsh.env["PATH"] = current_path + new_entries  # type: ignore
        return [str(entry) for entry in self.xsh.env["PATH"]]  # type: ignore

    def user(self) -> str:
        """
        Get the username of the current user.
        """
        return str(self.env("USER"))

    def env(self, name, set: object | None = None, force: bool = False) -> object:
        """
        Set an environment variable in the xonsh session.
        """
        if set is not None:
            if name in self.xsh.env and not force:
                print_warning(
                    f"Refusing to overwrite existing variable: {name}."
                    " If you want to explicitly overwrite it," 
                    " use the `force` parameter."
                )
                return self.xsh.env[name]  # type: ignore
            self.xsh.env[name] = set # type: ignore
        return self.xsh.env[name]  # type: ignore

    def prompt(self) -> PromptBuilder:
        """
        Set the prompt in the xonsh session.
        """
        try:
            return PromptBuilder(self.xsh)  # type: ignore
        except KeyError as e:
            raise ValueError("PROMPT_FIELDS not in env") from e

    def style(self) -> Style:
        """
        Create a new Style object
        """
        return Style()

    def add_style(self, name: str, style: Style) -> None:
        """
        Save the current style in the Xonfigz session.
        """
        self.style_map[name] = style

    @property
    def color(self) -> ColorNames:
        """
        Get the color names in the xonsh session.
        """
        return ColorNames()

    @property
    def ENV(self) -> dict:
        """
        Get the environment variables of the xonsh session.
        """
        return self.xsh.env  # type: ignore

    @property
    def width(self) -> int:
        """
        Get the width of the terminal.
        """
        return shutil.get_terminal_size().columns

    @property
    def height(self) -> int:
        """
        Get the height of the terminal.
        """
        return shutil.get_terminal_size().lines
