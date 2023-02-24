from integration.pymake_helpers import PyMakeHelpers
from pathlib import Path

class TestSample1:
    # Path to sample 1
    project_dir = Path.joinpath(
        Path(__file__).parent,
        "../../samples/1-hello-world"
    ).absolute().resolve()

    def test_cmake_314_build_debug(self):
        build_type = "debug"

        # Clean any pre-existing files
        helpers = PyMakeHelpers(self.project_dir)
        helpers.clean()

        # Run the build
        result = helpers.build(build_type, ["--cmake-version", "3.14"])
        assert result == 0

        # Verify that the output binary was created
        assert helpers.find_installed_file("HelloWorld", build_type)


    def test_cmake_314_build_release(self):
        build_type = "release"

        # Clean any pre-existing files
        helpers = PyMakeHelpers(self.project_dir)
        helpers.clean()

        # Run the build
        result = helpers.build(build_type, ["--cmake-version", "3.14"])
        assert result == 0

        # Verify that the output binary was created
        assert helpers.find_installed_file("HelloWorld", build_type)


    def test_cmake_325_build_debug(self):
        build_type = "debug"

        # Clean any pre-existing files
        helpers = PyMakeHelpers(self.project_dir)
        helpers.clean()

        # Run the build
        result = helpers.build(build_type, ["--cmake-version", "3.25"])
        assert result == 0

        # Verify that the output binary was created
        assert helpers.find_installed_file("HelloWorld", build_type)

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

        # Verify that the output binary was created
        assert helpers.find_installed_file("HelloWorld", build_type)

        # Also check for the CMake presets file
        assert helpers.find_generated_file("CMakePresets.json")
