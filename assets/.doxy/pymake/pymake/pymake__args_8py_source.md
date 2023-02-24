
# File pymake\_args.py

[**File List**](files.md) **>** [**core**](dir_b275da0bd59d7f0b7cbb72771801f871.md) **>** [**pymake\_args.py**](pymake__args_8py.md)

[Go to the documentation of this file.](pymake__args_8py.md) 

```Python

from argparse import Namespace

class PyMakeArgs(Namespace):
    """
    Stores arguments passed to PyMake.
    """
    def __init__(self, verbose: bool, presets: list[str]) -> None:
        """
        Initializes the PyMake arguments.
        @param verbose Whether verbose output should be enabled.
        @param presets Names of presets to enable.
        """
        self.verboseverbose = verbose
        self.presetspresets = presets

```