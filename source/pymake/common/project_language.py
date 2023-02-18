from enum import IntEnum

class EProjectLanguage(IntEnum):
    """
    Enum for the various languages a CMake project may use.
    """
    # C++
    Cpp = 0

    def to_cmake_language(self) -> str:
        """
        Converts an enum value to the equivalent CMake string.
        @returns The CMake string corresponding to the language. This string
          will be one of the valid options for the CMake `project()` method's
          `LANGUAGES` section.
        """
        if self == EProjectLanguage.Cpp:
            return "CXX"
        else:
            raise NotImplementedError()
