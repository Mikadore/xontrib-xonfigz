from typing import TYPE_CHECKING

import xontrib_xonfigz.xonfigz

if TYPE_CHECKING:
    from xonsh.built_ins import XonshSession  # type: ignore


def _load_xontrib_(xsh: XonshSession, **_):  # pyright: ignore[reportUnusedFunction]
    # If your xontrib was made only for interactive mode it's good practice
    #  to check this before executing.
    assert xsh is not None
    assert xsh.env is not None
    print("Autoloading xontrib `xonfigz`")
    xsh.ctx.update({"_XONFIGZ_INSTANCE": xontrib_xonfigz.xonfigz.Xonfigz(xsh)})

    return {"Xonfigz": xontrib_xonfigz.xonfigz.Xonfigz}
    # from .event_hooks import listen_cd
    # xsh.builtins.events.on_chdir(listen_cd)
