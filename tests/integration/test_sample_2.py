from integration.pymake_helpers import PyMakeHelpers
from pathlib import Path
from pymake.util.platform_statics import PlatformStatics

class TestSample2:
    # Path to sample 2
    project_dir = Path.joinpath(
        Path(__file__).parent,
        "../../samples/2-hello-static"
    ).absolute().resolve()

    def test_cmake_314_build_debug(self):
        build_type = "debug"

        # Clean any pre-existing files
        helpers = PyMakeHelpers(self.project_dir)
        helpers.clean()

        # Run the build
        result = helpers.build(build_type, ["--cmake-version", "3.14"])
        assert result == 0

        # Verify that the output binaries were created
        assert helpers.find_installed_file(
            PlatformStatics.get_static_lib_name("foo"),
            build_type
        )
        assert helpers.find_installed_file(
            PlatformStatics.get_executable_name("bar"),
            build_type
        )


    def test_cmake_314_build_release(self):
        build_type = "release"

        # Clean any pre-existing files
        helpers = PyMakeHelpers(self.project_dir)
        helpers.clean()

        # Run the build
        result = helpers.build(build_type, ["--cmake-version", "3.14"])
        assert result == 0

        # Verify that the output binaries were created
        assert helpers.find_installed_file(
            PlatformStatics.get_static_lib_name("foo"),
            build_type
        )
        assert helpers.find_installed_file(
            PlatformStatics.get_executable_name("bar"),
            build_type
        )


    def test_cmake_325_build_debug(self):
        build_type = "debug"

        # Clean any pre-existing files
        helpers = PyMakeHelpers(self.project_dir)
        helpers.clean()

        # Run the build
        result = helpers.build(build_type, ["--cmake-version", "3.25"])
        assert result == 0

        # Verify that the output binaries were created
        assert helpers.find_installed_file(
            PlatformStatics.get_static_lib_name("foo"),
            build_type
        )
        assert helpers.find_installed_file(
            PlatformStatics.get_executable_name("bar"),
            build_type
        )

        # Also check for the CMake presets file
        assert helpers.find_generated_file("CMakePresets.json")


    def test_cmake_325_build_release(self):
        build_type = "release"

        # Clean any pre-existing files
        helpers = PyMakeHelpers(self.project_dir)
        helpers.clean()

        # Run the build
        result = helpers.build(build_type, ["--cmake-version", "3.25"])
        assert result == 0

        # Verify that the output binaries were created
        assert helpers.find_installed_file(
            PlatformStatics.get_static_lib_name("foo"),
            build_type
        )
        assert helpers.find_installed_file(
            PlatformStatics.get_executable_name("bar"),
            build_type
        )

        # Also check for the CMake presets file
        assert helpers.find_generated_file("CMakePresets.json")


    def test_run_debug_binary(self):
        build_type = "debug"

        # Clean any pre-existing files
        helpers = PyMakeHelpers(self.project_dir)
        helpers.clean()

        # Run the build
        result = helpers.build(build_type, ["--cmake-version", "3.14"])
        assert result == 0

        # Verify that the output binary was created
        assert helpers.find_installed_file("bar", build_type)

        # Run the binary
        was_found, result, output = helpers.run_binary("bar")
        assert was_found
        assert result == 0
        assert output.strip() == "foo() = 42"


    def test_run_release_binary(self):
        build_type = "release"

        # Clean any pre-existing files
        helpers = PyMakeHelpers(self.project_dir)
        helpers.clean()

        # Run the build
        result = helpers.build(build_type, ["--cmake-version", "3.14"])
        assert result == 0

        # Verify that the output binary was created
        assert helpers.find_installed_file("bar", build_type)

        # Run the binary
        was_found, result, output = helpers.run_binary("bar")
        assert was_found
        assert result == 0
        assert output.strip() == "foo() = 42"
