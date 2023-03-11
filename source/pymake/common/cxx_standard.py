from enum import IntEnum

class ECxxStandard(IntEnum):
    """
    Enumeration of C++ standards supported for projects.
    """
    ## C++98
    Cpp98 = 98

    ## C++11
    Cpp11 = 11

    ## C++14
    Cpp14 = 14

    ## C++17
    # Requires CMake 3.8 or later.
    Cpp17 = 17

    ## C++20
    # Requires CMake 3.12 or later.
    Cpp20 = 20

    ## C++23
    # Requires CMake 3.20 or later.
    Cpp23 = 23

    ## C++26
    # Requires CMake 3.25 or later.
    # @remarks CMake's docs mention that this value is recognized as a valid
    #   value by CMake 3.25 and later, but no version has support for any C++26
    #   compiler yet.
    Cpp26 = 26
