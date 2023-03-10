from enum import IntEnum

class ETestFlags(IntEnum):
    """
    Represents the different type of test executables supported by PyMake.
    """
    ## Indicates that the test executable is not a test.
    NONE = 0x0

    ## Indicates that the test executable is a unit test.
    UNIT = 0x1

    ## Indicates that the test executable is an integration test.
    INTEGRATION = 0x2

    ## Indicates that the test executable has address sanitizer enabled.
    ADDRESS_SANITIZER = 0x10

    ## Indicates that the test executable has thread sanitizer enabled.
    THREAD_SANITIZER = 0x20

    ## @brief Indicates that the test executable has undefined behavior
    #  sanitizer enabled.
    UNDEFINED_BEHAVIOR_SANITIZER = 0x40

    ## Indicates that the test executable has leak sanitizer enabled.
    LEAK_SANITIZER = 0x80

    ## Indicates that the test executable has memory sanitizer enabled.
    MEMORY_SANITIZER = 0x100

    ## Indicates that the test executable has data flow sanitizer enabled.
    DATA_FLOW_SANITIZER = 0x200

    ## @brief Indicates that the test executable has control flow integrity
    #  sanitizer enabled.
    CONTROL_FLOW_INTEGRITY_SANITIZER = 0x400

    ## Indicates that the test executable has safe stack sanitizer enabled.
    SAFE_STACK_SANITIZER = 0x800

    ## Indicates that the test executable is invoked using Valgrind's memcheck.
    VALGRIND_MEMCHECK = 0x1000

    ## Indicates that the test executable is invoked using Valgrind's helgrind.
    VALGRIND_HELGRIND = 0x2000

    ## Indicates that the test executable is invoked using Valgrind's drd.
    VALGRIND_DRD = 0x4000
