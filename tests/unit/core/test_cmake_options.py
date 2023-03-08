from pymake.core.cmake_options import CMakeOptions

def test_properties_match_ctor_args():
    verbose = True
    cmake_options = CMakeOptions(verbose)
    assert cmake_options.verbose == verbose
