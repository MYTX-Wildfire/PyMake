from enum import IntEnum

class ESanitizerFlags(IntEnum):
    """
    Represents the sanitizers that can be enabled for a target.
    """
    ## Indicates that no sanitizers are enabled.
    NONE = 0x0

    ## Indicates that the address sanitizer is enabled.
    ADDRESS = 0x1

    ## Indicates that the thread sanitizer is enabled.
    THREAD = 0x2

    ## Indicates that the undefined behavior sanitizer is enabled.
    UNDEFINED_BEHAVIOR = 0x4

    ## Indicates that the leak sanitizer is enabled.
    LEAK = 0x8

    ## Indicates that the memory sanitizer is enabled.
    MEMORY = 0x10

    ## Indicates that the data flow sanitizer is enabled.
    DATA_FLOW = 0x20

    ## Indicates that the control flow integrity sanitizer is enabled.
    CONTROL_FLOW_INTEGRITY = 0x40

    ## Indicates that the safe stack sanitizer is enabled.
    SAFE_STACK = 0x80
