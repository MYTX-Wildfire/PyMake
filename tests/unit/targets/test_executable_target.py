from pathlib import Path
from pymake.common.scope import EScope
from pymake.common.target_type import ETargetType
from pymake.core.build_script_set import BuildScriptSet
from pymake.targets.executable_target import ExecutableTarget
from pymake.generators.yaml_file_generator import YamlFileGenerator
from pymake.tracing.null_caller_info_formatter import NullCallerInfoFormatter
from typing import Any


class TestExecutableTarget:
    build_script_set = BuildScriptSet(
        Path("/source"),
        Path("/generated"),
        NullCallerInfoFormatter()
    )


    def test_executable_target_sets_target_type_correctly(self):
        target = ExecutableTarget(self.build_script_set, "foo")
        assert target.target_type == ETargetType.EXECUTABLE


    def test_generate_cmake_code(self):
        """
        Verifies that creating an executable target generates the appropriate CMake code.
        """
        target_name = "foo"
        target = ExecutableTarget(self.build_script_set, target_name)
        target.generate_declaration()
        assert self.build_script_set
        assert len(self.build_script_set) == 1

        build_script = self.build_script_set.get_or_add_build_script()
        code = build_script.generator.generate()
        assert code
        assert "add_executable" in code
        assert target_name in code


    def test_target_not_installed_by_default(self):
        target = ExecutableTarget(self.build_script_set, "foo")
        assert not target.is_installed


    def test_target_installed_when_marked_as_installed(self):
        target = ExecutableTarget(self.build_script_set, "foo")
        target.install()
        assert target.is_installed


    def test_target_installed_to_cmake_default_path(self):
        target = ExecutableTarget(self.build_script_set, "foo")
        target.install()
        assert target.is_installed
        assert not target.install_path


    def test_target_installed_to_custom_path(self):
        target = ExecutableTarget(self.build_script_set, "foo")
        install_path = "/install/path"
        target.install(install_path)
        assert target.is_installed
        assert target.install_path == install_path


    def test_target_name_matches_ctor_arg(self):
        target_name = "foo"
        target = ExecutableTarget(self.build_script_set, target_name)
        assert target.target_name == target_name


    def test_target_sources_empty_by_default(self):
        target = ExecutableTarget(self.build_script_set, "foo")
        assert not target.sources


    def test_add_single_public_source(self):
        target = ExecutableTarget(self.build_script_set, "foo")
        source_path = "/source/foo.cpp"
        target.add_sources(source_path, EScope.PUBLIC)
        assert target.sources.public
        assert Path(source_path) in target.sources.public


    def test_add_multiple_public_sources(self):
        target = ExecutableTarget(self.build_script_set, "foo")
        source_paths = ["/source/foo.cpp", "/source/bar.cpp"]
        target.add_sources(source_paths, EScope.PUBLIC)
        assert target.sources.public
        assert Path(source_paths[0]) in target.sources.public
        assert Path(source_paths[1]) in target.sources.public


    def test_add_single_interface_source(self):
        target = ExecutableTarget(self.build_script_set, "foo")
        source_path = "/source/foo.cpp"
        target.add_sources(source_path, EScope.INTERFACE)
        assert target.sources.interface
        assert Path(source_path) in target.sources.interface


    def test_add_multiple_interface_sources(self):
        target = ExecutableTarget(self.build_script_set, "foo")
        source_paths = ["/source/foo.cpp", "/source/bar.cpp"]
        target.add_sources(source_paths, EScope.INTERFACE)
        assert target.sources.interface
        assert Path(source_paths[0]) in target.sources.interface
        assert Path(source_paths[1]) in target.sources.interface


    def test_add_single_private_source(self):
        target = ExecutableTarget(self.build_script_set, "foo")
        source_path = "/source/foo.cpp"
        target.add_sources(source_path, EScope.PRIVATE)
        assert target.sources.private
        assert Path(source_path) in target.sources.private


    def test_add_multiple_private_sources(self):
        target = ExecutableTarget(self.build_script_set, "foo")
        source_paths = ["/source/foo.cpp", "/source/bar.cpp"]
        target.add_sources(source_paths, EScope.PRIVATE)
        assert target.sources.private
        assert Path(source_paths[0]) in target.sources.private
        assert Path(source_paths[1]) in target.sources.private


    def test_add_source_by_abs_path(self):
        target = ExecutableTarget(self.build_script_set, "foo")
        source_path = "/source/foo.cpp"
        target.add_sources(source_path, EScope.PUBLIC)
        assert target.sources.public
        assert Path(source_path) in target.sources.public


    def test_add_source_by_rel_path(self):
        target = ExecutableTarget(self.build_script_set, "foo")
        source_path = "foo.cpp"
        target.add_sources(source_path, EScope.PUBLIC)
        assert target.sources.public
        assert Path(__file__).parent.joinpath(source_path) in target.sources.public


    def test_trace_file_includes_all_properties(self, tmp_path: Any):
        # Values used by the test
        target_name = "foo"
        sources = ["foo.cpp", "bar.cpp", "baz.cpp"]
        includes = [ "include1", "include2", "include3" ]
        libraries = [ "lib1", "lib2", "lib3" ]
        install_path = "/install/path"

        # Set up the target
        target = ExecutableTarget(self.build_script_set, target_name)
        indices = [0, 1, 2]
        scopes = [EScope.PUBLIC, EScope.PRIVATE, EScope.INTERFACE]

        for index, scope in zip(indices, scopes):
            target.add_sources(sources[index], scope)
            target.add_include_directories(includes[index], scope)
            target.link_to_library(libraries[index], False, False, scope)
        target.install(install_path)

        # Generate the trace file
        generator = YamlFileGenerator()
        output_path = Path(tmp_path).joinpath("target.yaml")
        target.generate_trace_file(output_path, generator)

        # Validate the trace file
        assert output_path.exists()
        with open(output_path) as f:
            contents = f.read()

        assert contents
        assert target_name in contents
        assert ETargetType.EXECUTABLE.value in contents
        for source in sources:
            assert source in contents
        for include in includes:
            assert include in contents
        for library in libraries:
            assert library in contents
        assert install_path in contents
