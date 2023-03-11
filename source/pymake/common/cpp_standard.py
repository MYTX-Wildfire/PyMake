from enum import Enum

class ECppStandard(Enum):
    """
    Enumeration of C++ standards supported for projects.
    """
    ## C++11
    Cpp11 = 11

    ## C++14
    Cpp14 = 14

    ## C++17
    Cpp17 = 17

    ## C++20
    Cpp20 = 20

    ## Latest C++ standard supported by the compiler.
    Latest = 0
