
import subprocess
import tempfile

from dndbuddy_core import settings


def paged(text):
    """
    Source: https://chase-seibert.github.io/blog/2012/10/31/python-fork-exec-vim-raw-input.html#
    """
    if not settings.TRY_PAGER:
        print(text)
        return

    try:
        with tempfile.NamedTemporaryFile("w") as f:
            f.write(text)
            f.flush()
            p = subprocess.Popen(["/usr/bin/less", f.name])
            p.wait()
    except KeyboardInterrupt:
        pass
