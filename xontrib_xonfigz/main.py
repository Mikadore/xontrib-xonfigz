from typing import TYPE_CHECKING

from xontrib_xonfigz.xonfigz import Xonfigz

if TYPE_CHECKING:
    from xonsh.built_ins import XonshSession  # type: ignore


def _load_xontrib_(xsh: XonshSession, **_):  # pyright: ignore[reportUnusedFunction]
    # If your xontrib was made only for interactive mode it's good practice
    #  to check this before executing.
    assert xsh is not None
    assert xsh.env is not None
    print("Autoloading xontrib `xonfigz`")
    Xonfigz.initialize(xsh)
    

    return {"Xonfigz": Xonfigz}
    # from .event_hooks import listen_cd
    # xsh.builtins.events.on_chdir(listen_cd)
