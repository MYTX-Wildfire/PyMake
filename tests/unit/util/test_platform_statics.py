from pymake.util.platform_statics import PlatformStatics
import sys

# Most of these tests are redundant given the current implementation of
#   PlatformStatics. They're included to avoid needing to add 'pragma: no cover'
#   to the methods in PlatformStatics and to ensure that the methods' behavior
#   does not change even if the implementation changes.

def test_check_current_os():
    assert PlatformStatics.is_linux() == ("linux" in sys.platform)
    assert PlatformStatics.is_windows() == ("win" in sys.platform)
    assert PlatformStatics.is_macos() == ("darwin" in sys.platform)


def test_check_current_os_is_unix():
    assert PlatformStatics.is_unix() == \
        (PlatformStatics.is_linux() or PlatformStatics.is_macos())


def test_static_lib_prefix():
    if PlatformStatics.is_windows():
        assert PlatformStatics.static_lib_prefix() == ""
    else:
        assert PlatformStatics.static_lib_prefix() == "lib"


def test_static_lib_suffix():
    if PlatformStatics.is_windows():
        assert PlatformStatics.static_lib_suffix() == ".lib"
    else:
        assert PlatformStatics.static_lib_suffix() == ".a"


def test_static_lib_name():
    if PlatformStatics.is_windows():
        assert PlatformStatics.get_static_lib_name("foo") == "foo.lib"
    else:
        assert PlatformStatics.get_static_lib_name("foo") == "libfoo.a"


def test_shared_lib_prefix():
    if PlatformStatics.is_windows():
        assert PlatformStatics.shared_lib_prefix() == ""
    else:
        assert PlatformStatics.shared_lib_prefix() == "lib"


def test_shared_lib_suffix():
    if PlatformStatics.is_windows():
        assert PlatformStatics.shared_lib_suffix() == ".dll"
    elif PlatformStatics.is_macos():
        assert PlatformStatics.shared_lib_suffix() == ".dylib"
    else:
        assert PlatformStatics.shared_lib_suffix() == ".so"


def test_shared_lib_name():
    if PlatformStatics.is_windows():
        assert PlatformStatics.get_shared_lib_name("foo") == "foo.dll"
    elif PlatformStatics.is_macos():
        assert PlatformStatics.get_shared_lib_name("foo") == "libfoo.dylib"
    else:
        assert PlatformStatics.get_shared_lib_name("foo") == "libfoo.so"
