import shutil

from xonsh.built_ins import XonshSession  # type: ignore  # noqa: TC002

from xontrib_xonfigz.prompt import PromptBuilder

_XONFIGZ_INSTANCE: Xonfigz | None = None


class Xonfigz:
    xsh: XonshSession

    def __init__(self, xsh: XonshSession):
        if xsh is None:
            raise ValueError("XonshSession cannot be None")
        if xsh.env is None:
            raise ValueError("XonshSession.env cannot be None")
        self.xsh = xsh

    @staticmethod
    def instance() -> Xonfigz:
        """
        Get the current instance of Xonfigz.
        """
        global _XONFIGZ_INSTANCE
        if _XONFIGZ_INSTANCE is None:
            raise ValueError("Xonfigz instance has not been created yet.")
        return _XONFIGZ_INSTANCE

    def home(self, path: str | None = None) -> str:
        """
        Get the home directory of the current user.
        If path is provided, it will be joined to the home directory.
        """
        if path is None:
            return str(self.xsh.env["HOME"])  # type: ignore
        else:
            self.set_env("HOME", path)
        return str(self.xsh.env["HOME"])  # type: ignore

    def set_env(self, name, set: object) -> Xonfigz:
        """
        Set an environment variable in the xonsh session.
        """
        self.xsh.env[name] = set  # type: ignore
        return self

    def prompt(self) -> PromptBuilder:
        """
        Set the prompt in the xonsh session.
        """
        try:
            return PromptBuilder(self.xsh.env["PROMPT_FIELDS"])  # type: ignore
        except KeyError as e:
            raise ValueError("PROMPT_FIELDS not in env") from e

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
