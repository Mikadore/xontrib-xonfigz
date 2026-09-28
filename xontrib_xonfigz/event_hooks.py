def activate_env(path: str):
    # lazy import to reduce startup cost
    from xontrib.voxapi import Vox  # type: ignore

    vox = Vox()  # type: ignore
    vox.activate(path)  # type: ignore


def listen_cd(olddir, newdir, **_):  # type: ignore
    activate_env(newdir)  # type: ignore
