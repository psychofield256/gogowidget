import os
import sys

def restart():
    """
    Restart function.

    Note: the function doesn't return.
    Even a context manager will be stopped.
    """
    python = sys.executable
    os.execl(python, python, *sys.argv)
