from pymake.tracing.caller_info import CallerInfo
from pymake.tracing.traced import ITraced

class DummyTraced(ITraced):
    """
    Helper class that implements `ITraced`.
    """
    def __init__(self, origin: CallerInfo):
        """
        Initializes the instance.
        @param origin Value to store as the origin of the object.
        """
        self._origin = origin

    @property
    def origin(self) -> CallerInfo:
        """
        Gets the location that constructed the object.
        """
        return self._origin
