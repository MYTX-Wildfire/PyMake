import sys

class PlatformStatics:
    """
    Provides statics for the current platform.
    """

    @staticmethod
    def is_windows() -> bool:
        """
        Gets whether the platform is Windows.
        @returns True if the platform is Windows, False otherwise.
        """
        return sys.platform.startswith("win")


    @staticmethod
    def is_linux() -> bool:
        """
        Gets whether the platform is Linux.
        @returns True if the platform is Linux, False otherwise.
        """
        return sys.platform.startswith("linux")


    @staticmethod
    def is_macos() -> bool:
        """
        Gets whether the platform is macOS.
        @returns True if the platform is macOS, False otherwise.
        """
        return sys.platform.startswith("darwin")


    @staticmethod
    def is_unix() -> bool:
        """
        Gets whether the platform is Unix.
        @returns True if the platform is a Unix platform, False otherwise.
        """
        return PlatformStatics.is_linux() or PlatformStatics.is_macos()


    @staticmethod
    def static_lib_prefix() -> str:
        """
        Gets the prefix for static libraries.
        @returns The prefix for static libraries.
        """
        if PlatformStatics.is_windows():
            return ""
        return "lib"


    @staticmethod
    def static_lib_suffix() -> str:
        """
        Gets the extension for static libraries.
        @returns The extension for static libraries.
        """
        if PlatformStatics.is_windows():
            return ".lib"
        return ".a"


    @staticmethod
    def shared_lib_prefix() -> str:
        """
        Gets the prefix for shared libraries.
        @returns The prefix for shared libraries.
        """
        if PlatformStatics.is_windows():
            return ""
        return "lib"


    @staticmethod
    def shared_lib_suffix() -> str:
        """
        Gets the extension for shared libraries.
        @returns The extension for shared libraries.
        """
        if PlatformStatics.is_windows():
            return ".dll"
        return ".so"
