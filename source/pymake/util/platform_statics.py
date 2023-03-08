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
            # Code coverage is recorded on Linux; ignore non-Linux branches
            return "" # pragma: no cover
        return "lib"


    @staticmethod
    def static_lib_suffix() -> str:
        """
        Gets the extension for static libraries.
        @returns The extension for static libraries.
        """
        if PlatformStatics.is_windows():
            # Code coverage is recorded on Linux; ignore non-Linux branches
            return ".lib" # pragma: no cover
        return ".a"


    @staticmethod
    def get_static_lib_name(name: str) -> str:
        """
        Gets the name of a static library.
        @param name Name of the library, minus any prefix or suffix.
        @returns The name of the static library.
        """
        return PlatformStatics.static_lib_prefix() + name + \
            PlatformStatics.static_lib_suffix()


    @staticmethod
    def shared_lib_prefix() -> str:
        """
        Gets the prefix for shared libraries.
        @returns The prefix for shared libraries.
        """
        if PlatformStatics.is_windows():
            # Code coverage is recorded on Linux; ignore non-Linux branches
            return "" # pragma: no cover
        return "lib"


    @staticmethod
    def shared_lib_suffix() -> str:
        """
        Gets the extension for shared libraries.
        @returns The extension for shared libraries.
        """
        # Code coverage is recorded on Linux; ignore non-Linux branches
        if PlatformStatics.is_windows():
            return ".dll" # pragma: no cover
        elif PlatformStatics.is_macos():
            return ".dylib" # pragma: no cover
        return ".so"


    @staticmethod
    def get_shared_lib_name(name: str) -> str:
        """
        Gets the name of a shared library.
        @param name Name of the library, minus any prefix or suffix.
        @returns The name of the shared library.
        """
        return PlatformStatics.shared_lib_prefix() + name + \
            PlatformStatics.shared_lib_suffix()
