
import os


def load_flag(name):
    return os.environ.get(name, "").lower() not in ("0", "no", "off", "false")


def load_list(name, default=None):
    try:
        return [each.strip() for each in os.environ[name].split(",")]
    except KeyError:
        return default


DEFAULT_MODULES = [
    "dndbuddy_basic",
    "dndbuddy_phb",
]

ANSI_COLORS = load_flag("DND_ANSI_COLORS")
TRY_PAGER = load_flag("DND_TRY_PAGER")
MODULE_NAMES = load_list("DND_MODULES", DEFAULT_MODULES)
