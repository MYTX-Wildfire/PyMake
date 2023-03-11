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
        self.verbose = verbose
        self.presets = presets
