from typing import Any

from xonsh.built_ins import XonshSession

from xontrib_xonfigz.color import Style  # type: ignore  # noqa: TC002


class PromptFields:
    """
    Represents the fields that can be used in a prompt.
    """

    xsh: XonshSession

    def __init__(self, xsh: XonshSession):
        self.xsh = xsh

    @property
    def render_user(self) -> str:
        """The username of the current user"""
        return self.fields["user"]

    @property
    def render_hostname(self) -> str:
        """The name of the host computer"""
        return self.fields["hostname"]

    @property
    def render_cwd(self) -> str:
        """
        The current working directory. Use $DYNAMIC_CWD_WIDTH
        to set a maximum width and $DYNAMIC_CWD_ELISION_CHAR for the elision character.
        """
        return self.fields["cwd"]

    @property
    def render_short_cwd(self) -> str:
        """
        A shortened form of the current working directory;
        e.g., /path/to/xonsh becomes /p/t/xonsh
        """
        return self.fields["short_cwd"]

    @property
    def render_cwd_dir(self) -> str:
        """The dirname of the current working directory, e.g. /path/to/"""
        return self.fields["cwd_dir"]

    @property
    def render_cwd_base(self) -> str:
        """The basename of the current working directory, e.g. xonsh"""
        return self.fields["cwd_base"]

    @property
    def render_env_name(self) -> str:
        """The name of active virtual environment, if any."""
        return self.fields["env_name"]

    @property
    def render_env_prefix(self) -> str:
        """Prefix characters for active virtual environment (default "(")."""
        return self.fields["env_prefix"]

    @property
    def render_env_postfix(self) -> str:
        """Postfix characters for active virtual environment (default ") ")."""
        return self.fields["env_postfix"]

    @property
    def render_curr_branch(self) -> str:
        """The name of the current git branch, if any."""
        return self.fields["curr_branch"]

    @property
    def render_branch_color(self) -> str:
        """
        {BOLD_GREEN} if the current git branch is clean, otherwise {BOLD_RED}.
        Yellow if undetermined.
        """
        return self.fields["branch_color"]

    @property
    def render_branch_bg_color(self) -> str:
        """Like {branch_color}, but sets a background color."""
        return self.fields["branch_bg_color"]

    @property
    def render_prompt_end(self) -> str:
        """@# if the user has root/admin permissions, @ otherwise."""
        return self.fields["prompt_end"]

    @property
    def render_current_job(self) -> str:
        """The name of the command currently running in the foreground."""
        return self.fields["current_job"]

    @property
    def render_gitstatus(self) -> str:
        """
        Informative git status, like [main|MERGING|+1…2].
        See xonsh.prompt.gitstatus for customization options."""
        return self.fields["gitstatus"]

    @property
    def render_localtime(self) -> str:
        """The current local time, formatted with time_format."""
        return self.fields["localtime"]

    @property
    def render_time_format(self) -> str:
        """A time format string, defaulting to "%H"""
        return self.fields["time_format"]

    @property
    def render_last_return_code(self) -> str:
        """The return code of the last issued command."""
        return self.fields["last_return_code"]

    @property
    def render_last_return_code_if_nonzero(self) -> str:
        """The return code if non-zero, otherwise None."""
        return self.fields["last_return_code_if_nonzero"]

    def __getattr__(self, name: str) -> Any:
        if name in self.fields:
            return self.fields[name]
        raise AttributeError(f"{name} not found in PROMPT_FIELDS")

    @property
    def user(self) -> str:
        """The username of the current user"""
        return "user"

    @property
    def hostname(self) -> str:
        """The name of the host computer"""
        return "hostname"

    @property
    def cwd(self) -> str:
        """
        The current working directory. Use $DYNAMIC_CWD_WIDTH
        to set a maximum width and $DYNAMIC_CWD_ELISION_CHAR for the elision character.
        """
        return "cwd"

    @property
    def short_cwd(self) -> str:
        """
        A shortened form of the current working directory;
        e.g., /path/to/xonsh becomes /p/t/xonsh
        """
        return "short_cwd"

    @property
    def cwd_dir(self) -> str:
        """The dirname of the current working directory, e.g. /path/to/"""
        return "cwd_dir"

    @property
    def cwd_base(self) -> str:
        """The basename of the current working directory, e.g. xonsh"""
        return "cwd_base"

    @property
    def env_name(self) -> str:
        """The name of active virtual environment, if any."""
        return "env_name"

    @property
    def env_prefix(self) -> str:
        """Prefix characters for active virtual environment (default "(")."""
        return "env_prefix"

    @property
    def env_postfix(self) -> str:
        """Postfix characters for active virtual environment (default ") ")."""
        return "env_postfix"

    @property
    def curr_branch(self) -> str:
        """The name of the current git branch, if any."""
        return "curr_branch"

    @property
    def branch_color(self) -> str:
        """
        {BOLD_GREEN} if the current git branch is clean, otherwise {BOLD_RED}.
        Yellow if undetermined.
        """
        return "branch_color"

    @property
    def branch_bg_color(self) -> str:
        """Like {branch_color}, but sets a background color."""
        return "branch_bg_color"

    @property
    def prompt_end(self) -> str:
        """@# if the user has root/admin permissions, @ otherwise."""
        return "prompt_end"

    @property
    def current_job(self) -> str:
        """The name of the command currently running in the foreground."""
        return "current_job"

    @property
    def gitstatus(self) -> str:
        """
        Informative git status, like [main|MERGING|+1…2].
        See xonsh.prompt.gitstatus for customization options.
        """
        return "gitstatus"

    @property
    def localtime(self) -> str:
        """The current local time, formatted with time_format."""
        return "localtime"

    @property
    def time_format(self) -> str:
        """A time format string, defaulting to "%H"""
        return "time_format"

    @property
    def last_return_code(self) -> str:
        """The return code of the last issued command."""
        return "last_return_code"

    @property
    def last_return_code_if_nonzero(self) -> str:
        """The return code if non-zero, otherwise None."""
        return "last_return_code_if_nonzero"


class PromptBuilder:
    xsh: XonshSession
    fields: PromptFields
    prompt: str
    _style: Style

    def __init__(self, xsh: XonshSession):
        self.xsh = xsh
        self.fields = PromptFields(xsh)
        self.prompt = ""
        self._style = Style(background=None, foreground=None)

    def style(self, style: Style) -> PromptBuilder:
        """
        Set the current style for the prompt.
        """
        self.prompt += self._style.reset_modifiers()
        self.prompt += style.render_modifiers()
        self.prompt += style.render_color()
        self._style = style

        return self

    def reset_style(self) -> PromptBuilder:
        """
        Reset the current style for the prompt.
        """
        self.prompt += self._style.reset_modifiers()
        self._style = Style(background=None, foreground=None)
        self.prompt += self._style.render_color()
        return self

    def add(self, text: str) -> PromptBuilder:
        """
        Push a raw string to the prompt, without
        rendering any fields.
        """
        self.prompt += text
        return self

    def render(self) -> str:
        """
        Install the prompt in the xonsh session.
        """
        self.prompt += self._style.reset_modifiers()
        return self.prompt
    
    @property
    def f(self) -> PromptFields:
        """
        Returns the PromptFields object for the current xonsh session.
        """
        return self.fields
