from . import _diffwoodcore as m


def is_available() -> bool:
    return m.cuda_is_available()

