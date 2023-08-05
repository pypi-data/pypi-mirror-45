from contextlib import contextmanager
from ._gill import lock_gil, unlock_gil


__all__ = ["locked_gil"]


@contextmanager
def locked_gil():
    lock_gil()
    try:
        yield
    finally:
        unlock_gil()
