class CMakeOptions:
    """
    Various CMake options that may be enabled via PyMake flags.
    """
    def __init__(self,
        verbose: bool):
        """
        Initializes the object.
        @param verbose Whether to pass --verbose to CMake.
        """
        self._verbose = verbose


    @property
    def verbose(self) -> bool:
        """
        Gets whether to pass --verbose to CMake.
        """
        return self._verbose
