from pathlib import Path
from pymake.common.scope import EScope
from pymake.common.target_type import ETargetType
from pymake.core.build_script_set import BuildScriptSet
from pymake.targets.executable_target import ExecutableTarget
from pymake.targets.target import ITarget
from pymake.targets.static_library_target import StaticLibraryTarget
from pymake.tracing.caller_info import CallerInfo
from pymake.tracing.null_caller_info_formatter import NullCallerInfoFormatter
from pymake.util.platform_statics import PlatformStatics
import pytest
from typing import Any

class MockTarget(ITarget):
    def __init__(self,
        build_scripts: BuildScriptSet,
        target_name: str,
        target_type: ETargetType):
        super().__init__(
            build_scripts,
            target_name,
            target_type
        )

    def generate_declaration(self) -> None:
        pass

    def _create_empty_clone(self) -> ITarget:
        return self


class TestTarget:
    build_script_set = BuildScriptSet(
        Path("/source"),
        Path("/generated"),
        NullCallerInfoFormatter()
    )


    def test_target_name_matches_ctor_arg(self):
        target_name = "foo"
        target = MockTarget(
            self.build_script_set,
            target_name,
            ETargetType.EXECUTABLE
        )
        assert target.target_name == target_name


    def test_target_type_matches_ctor_arg(self):
        target_type = ETargetType.EXECUTABLE
        target = MockTarget(
            self.build_script_set,
            "foo",
            target_type
        )
        assert target.target_type == target_type


    def test_is_full_target(self):
        target = MockTarget(
            self.build_script_set,
            "foo",
            ETargetType.EXECUTABLE
        )
        assert not target.is_full_target


    def test_target_as_string(self):
        target_name = "foo"
        target = MockTarget(
            self.build_script_set,
            target_name,
            ETargetType.EXECUTABLE
        )
        assert str(target) == target_name


    def test_get_include_directories(self):
        # Verify that no include directories are returned initially
        target = MockTarget(
            self.build_script_set,
            "foo",
            ETargetType.EXECUTABLE
        )
        assert not target.include_directories

        # Add include directories to each scope
        public_include_dir = "/public/include"
        interface_include_dir = "/interface/include"
        private_include_dir = "/private/include"

        target.add_include_directories(public_include_dir, EScope.PUBLIC)
        target.add_include_directories(interface_include_dir, EScope.INTERFACE)
        target.add_include_directories(private_include_dir, EScope.PRIVATE)

        # Verify that the include directories are returned in the correct scope
        assert target.include_directories
        include_dirs = target.include_directories
        assert Path(public_include_dir) in \
            include_dirs.select_set(EScope.PUBLIC)
        assert Path(interface_include_dir) in \
            include_dirs.select_set(EScope.INTERFACE)
        assert Path(private_include_dir) in \
            include_dirs.select_set(EScope.PRIVATE)


    def test_add_duplicate_include_directory_ignored(self):
        target = MockTarget(
            self.build_script_set,
            "foo",
            ETargetType.EXECUTABLE
        )

        # If an include directory is added twice, only the original should be
        #   recorded
        include_dir = "/include"
        call_site = CallerInfo.closest_external_frame()
        target.add_include_directories(include_dir, EScope.PUBLIC)
        target.add_include_directories(include_dir, EScope.PUBLIC)

        include_dirs = target.include_directories.select_set(EScope.PUBLIC)
        assert len(include_dirs) == 1
        assert Path(include_dir) in include_dirs

        traced_include = include_dirs[Path(include_dir)]
        assert traced_include.origin.file_path == call_site.file_path
        assert traced_include.origin.line_number == (call_site.line_number + 1)


    def test_add_multiple_include_directories(self):
        target = MockTarget(
            self.build_script_set,
            "foo",
            ETargetType.EXECUTABLE
        )

        # If multiple include directories are added, they should all be
        #   recorded
        include_dir1 = "/include1"
        include_dir2 = "/include2"
        target.add_include_directories(
            [include_dir1, include_dir2],
            EScope.PUBLIC
        )

        include_dirs = target.include_directories.select_set(EScope.PUBLIC)
        assert len(include_dirs) == 2
        assert Path(include_dir1) in include_dirs
        assert Path(include_dir2) in include_dirs


    def test_add_include_directory_generates_cmake_code(self):
        target = MockTarget(
            self.build_script_set,
            "foo",
            ETargetType.EXECUTABLE
        )

        # If an include directory is added, it should be recorded in the
        #   generated CMake code
        include_dir = "/include"
        scope = EScope.PUBLIC
        target.add_include_directories(include_dir, scope)

        # Verify that CMake code was generated
        generator = self.build_script_set.get_or_add_build_script().generator
        cmake_code = generator.generate()
        assert "target_include_directories" in cmake_code
        assert include_dir in cmake_code
        assert scope.name in cmake_code


    def test_get_link_libraries(self):
        # Verify that no link libraries are returned initially
        target = MockTarget(
            self.build_script_set,
            "foo",
            ETargetType.EXECUTABLE
        )
        assert not target.link_libraries

        # Add libraries to each scope
        public_lib = "public_lib"
        interface_lib = "interface_lib"
        private_lib = "private_lib"

        target.link_to_library(public_lib, scope=EScope.PUBLIC)
        target.link_to_library(interface_lib, scope=EScope.INTERFACE)
        target.link_to_library(private_lib, scope=EScope.PRIVATE)

        # Verify that the libraries are returned in the correct scope
        assert target.link_libraries
        link_libs = target.link_libraries
        assert public_lib in link_libs.select_set(EScope.PUBLIC)
        assert interface_lib in link_libs.select_set(EScope.INTERFACE)
        assert private_lib in link_libs.select_set(EScope.PRIVATE)


    def test_add_duplicate_library_ignored(self):
        target = MockTarget(
            self.build_script_set,
            "foo",
            ETargetType.EXECUTABLE
        )

        # If a library is added twice, only the original should be recorded
        lib = "lib"
        call_site = CallerInfo.closest_external_frame()
        target.link_to_library(lib, scope=EScope.PUBLIC)
        target.link_to_library(lib, scope=EScope.PUBLIC)

        link_libs = target.link_libraries.select_set(EScope.PUBLIC)
        assert len(link_libs) == 1
        assert lib in link_libs

        traced_lib = link_libs[lib]
        assert traced_lib.origin.file_path == call_site.file_path
        assert traced_lib.origin.line_number == (call_site.line_number + 1)


    def test_add_platform_prefix_suffix_to_static_library(self):
        target = MockTarget(
            self.build_script_set,
            "foo",
            ETargetType.EXECUTABLE
        )

        # If a static library is added, the platform prefix and suffix should
        #   be added
        lib_name = "foo"
        full_lib_name = PlatformStatics.get_static_lib_name(lib_name)
        target.link_to_library(lib_name, True, False, scope=EScope.PUBLIC)

        link_libs = target.link_libraries.select_set(EScope.PUBLIC)
        assert len(link_libs) == 1
        assert full_lib_name in link_libs


    def test_add_platform_prefix_suffix_throws_if_static_library_is_path(self):
        target = MockTarget(
            self.build_script_set,
            "foo",
            ETargetType.EXECUTABLE
        )

        # If a library is added that is a path, the platform prefix and suffix
        #   should not be added
        lib_name = Path("/foo")
        with pytest.raises(ValueError):
            target.link_to_library(lib_name, True, False, scope=EScope.PUBLIC)


    def test_add_platform_prefix_suffix_to_shared_library(self):
        target = MockTarget(
            self.build_script_set,
            "foo",
            ETargetType.EXECUTABLE
        )

        # If a shared library is added, the platform prefix and suffix should
        #   be added
        lib_name = "foo"
        full_lib_name = PlatformStatics.get_shared_lib_name(lib_name)
        target.link_to_library(lib_name, False, True, scope=EScope.PUBLIC)

        link_libs = target.link_libraries.select_set(EScope.PUBLIC)
        assert len(link_libs) == 1
        assert full_lib_name in link_libs


    def test_add_platform_prefix_suffix_throws_if_shared_library_is_path(self):
        target = MockTarget(
            self.build_script_set,
            "foo",
            ETargetType.EXECUTABLE
        )

        # If a library is added that is a path, the platform prefix and suffix
        #   should not be added
        lib_name = Path("/foo")
        with pytest.raises(ValueError):
            target.link_to_library(lib_name, False, True, scope=EScope.PUBLIC)


    def test_add_library_as_path_resolved_to_abs_path(self):
        target = MockTarget(
            self.build_script_set,
            "foo",
            ETargetType.EXECUTABLE
        )

        # If a library is added as a path, it should be resolved to an
        #   absolute path
        lib_path = Path("../foo")
        target.link_to_library(lib_path, scope=EScope.PUBLIC)

        link_libs = target.link_libraries.select_set(EScope.PUBLIC)
        assert len(link_libs) == 1
        assert str(lib_path.resolve()) in link_libs


    def test_add_library_throws_if_shared_and_static(self):
        target = MockTarget(
            self.build_script_set,
            "foo",
            ETargetType.EXECUTABLE
        )

        # Setting both `is_static` and `is_shared` to true should throw
        with pytest.raises(ValueError):
            target.link_to_library("bar", True, True, scope=EScope.PUBLIC)


    def test_add_library_generates_cmake_code(self):
        target = MockTarget(
            self.build_script_set,
            "foo",
            ETargetType.EXECUTABLE
        )

        # If a library is added, it should be recorded in the generated CMake
        #   code
        lib = "lib"
        scope = EScope.PUBLIC
        target.link_to_library(lib, scope=scope)

        # Verify that CMake code was generated
        generator = self.build_script_set.get_or_add_build_script().generator
        cmake_code = generator.generate()
        assert "target_link_libraries" in cmake_code
        assert lib in cmake_code
        assert scope.name in cmake_code


    def test_link_to_target(self):
        # Create the targets to use
        public_lib_target = MockTarget(
            self.build_script_set,
            "public-lib",
            ETargetType.STATIC
        )
        interface_lib_target = MockTarget(
            self.build_script_set,
            "interface-lib",
            ETargetType.STATIC
        )
        private_lib_target = MockTarget(
            self.build_script_set,
            "private-lib",
            ETargetType.STATIC
        )
        exe_target = MockTarget(
            self.build_script_set,
            "exe",
            ETargetType.EXECUTABLE
        )

        # Link the executable to the library
        exe_target.link_to_target(public_lib_target, EScope.PUBLIC)
        exe_target.link_to_target(interface_lib_target, EScope.INTERFACE)
        exe_target.link_to_target(private_lib_target, EScope.PRIVATE)

        # Verify that the executable is linked to the library
        assert public_lib_target in \
            exe_target.link_libraries.select_set(EScope.PUBLIC)
        assert interface_lib_target in \
            exe_target.link_libraries.select_set(EScope.INTERFACE)
        assert private_lib_target in \
            exe_target.link_libraries.select_set(EScope.PRIVATE)


    def test_link_to_duplicate_target_ignored(self):
        # Create the targets to use
        lib_target = MockTarget(
            self.build_script_set,
            "lib",
            ETargetType.STATIC
        )
        exe_target = MockTarget(
            self.build_script_set,
            "exe",
            ETargetType.EXECUTABLE
        )

        # Link the executable to the library
        call_site = CallerInfo.closest_external_frame()
        exe_target.link_to_target(lib_target, EScope.PUBLIC)
        exe_target.link_to_target(lib_target, EScope.PUBLIC)

        # Verify that the executable is linked to the library
        link_libraries = exe_target.link_libraries.select_set(EScope.PUBLIC)
        assert lib_target in link_libraries
        traced_target = link_libraries[lib_target]
        assert traced_target.origin.file_path == call_site.file_path
        assert traced_target.origin.line_number == (call_site.line_number + 1)


    def test_link_to_executable_target_throws(self):
        # Create the targets to use
        exe_target = MockTarget(
            self.build_script_set,
            "exe",
            ETargetType.EXECUTABLE
        )
        other_exe_target = MockTarget(
            self.build_script_set,
            "other-exe",
            ETargetType.EXECUTABLE
        )

        # Link the executable to the library
        with pytest.raises(ValueError):
            exe_target.link_to_target(other_exe_target, EScope.PUBLIC)


    def test_link_to_target_generates_cmake_code(self):
        # Create the targets to use
        lib_target = MockTarget(
            self.build_script_set,
            "lib",
            ETargetType.STATIC
        )
        exe_target = MockTarget(
            self.build_script_set,
            "exe",
            ETargetType.EXECUTABLE
        )

        # Link the executable to the library
        exe_target.link_to_target(lib_target, EScope.PUBLIC)

        # Verify that CMake code was generated
        generator = self.build_script_set.get_or_add_build_script().generator
        cmake_code = generator.generate()
        assert "target_link_libraries" in cmake_code
        assert lib_target.target_name in cmake_code
        assert EScope.PUBLIC.name in cmake_code


    def test_get_sources(self):
        # Verify that no sources are returned initially
        target = MockTarget(
            self.build_script_set,
            "foo",
            ETargetType.EXECUTABLE
        )
        assert not target.sources

        # Add sources to each scope
        public_src = "/public/src"
        interface_src = "/interface/src"
        private_src = "/private/src"

        target.add_sources(public_src, EScope.PUBLIC)
        target.add_sources(interface_src, EScope.INTERFACE)
        target.add_sources(private_src, EScope.PRIVATE)

        # Verify that the sources are returned in the correct scope
        assert target.sources
        sources = target.sources
        assert Path(public_src) in sources.select_set(EScope.PUBLIC)
        assert Path(interface_src) in sources.select_set(EScope.INTERFACE)
        assert Path(private_src) in sources.select_set(EScope.PRIVATE)


    def test_add_multiple_sources(self):
        target = MockTarget(
            self.build_script_set,
            "foo",
            ETargetType.EXECUTABLE
        )

        # If multiple sources are added, they should all be recorded
        src1 = "/src1"
        src2 = "/src2"
        target.add_sources([src1, src2], EScope.PUBLIC)

        sources = target.sources.select_set(EScope.PUBLIC)
        assert len(sources) == 2
        assert Path(src1) in sources
        assert Path(src2) in sources


    def test_add_duplicate_source_ignored(self):
        target = MockTarget(
            self.build_script_set,
            "foo",
            ETargetType.EXECUTABLE
        )

        # If a source is added twice, only the original should be recorded
        src = "/src"
        call_site = CallerInfo.closest_external_frame()
        target.add_sources(src, EScope.PUBLIC)
        target.add_sources(src, EScope.PUBLIC)

        sources = target.sources.select_set(EScope.PUBLIC)
        assert len(sources) == 1
        assert Path(src) in sources

        traced_src = sources[Path(src)]
        assert traced_src.origin.file_path == call_site.file_path
        assert traced_src.origin.line_number == (call_site.line_number + 1)


    def test_duplicate_install_call_ignored(self, tmp_path: Any):
        target = MockTarget(
            self.build_script_set,
            "foo",
            ETargetType.EXECUTABLE
        )

        # The second install call should be ignored
        target.install()
        target.install()
        assert target.is_installed


    def test_traced_dict_contains_inherited_properties(self):
        # Create the targets to use
        lib_target = StaticLibraryTarget(
            self.build_script_set,
            "lib"
        )
        exe_target = ExecutableTarget(
            self.build_script_set,
            "exe"
        )

        # Link the executable to the library
        exe_target.link_to_target(lib_target, EScope.PRIVATE)

        # Add properties to the library target
        # Since PyMake uses late binding when resolving inherited properties,
        #   the executable target should still receive these properties
        public_include_dir = "/public/include/dir"
        interface_include_dir = "/interface/include/dir"
        private_include_dir = "/private/include/dir"

        lib_target.add_include_directories(public_include_dir, EScope.PUBLIC)
        lib_target.add_include_directories(interface_include_dir, EScope.INTERFACE)
        lib_target.add_include_directories(private_include_dir, EScope.PRIVATE)

        public_lib = "/public/lib"
        interface_lib = "/interface/lib"
        private_lib = "/private/lib"

        lib_target.link_to_library(public_lib, scope=EScope.PUBLIC)
        lib_target.link_to_library(interface_lib, scope=EScope.INTERFACE)
        lib_target.link_to_library(private_lib, scope=EScope.PRIVATE)

        public_source = "/public/source"
        interface_source = "/interface/source"
        private_source = "/private/source"

        lib_target.add_sources(public_source, EScope.PUBLIC)
        lib_target.add_sources(interface_source, EScope.INTERFACE)
        lib_target.add_sources(private_source, EScope.PRIVATE)

        # Verify that the executable target has inherited the properties (minus
        #   private properties)
        full_target = exe_target.get_full_target()
        assert full_target.include_directories
        assert full_target.link_libraries
        assert full_target.sources

        include_dirs = full_target.include_directories
        assert Path(public_include_dir) in include_dirs.select_set(EScope.PUBLIC)
        assert Path(interface_include_dir) in include_dirs.select_set(EScope.INTERFACE)
        assert Path(private_include_dir) not in include_dirs.select_set(EScope.PRIVATE)

        link_libs = full_target.link_libraries
        assert public_lib in link_libs.select_set(EScope.PUBLIC)
        assert interface_lib in link_libs.select_set(EScope.INTERFACE)
        assert private_lib not in link_libs.select_set(EScope.PRIVATE)

        sources = full_target.sources
        assert Path(public_source) in sources.select_set(EScope.PUBLIC)
        assert Path(interface_source) in sources.select_set(EScope.INTERFACE)
        assert Path(private_source) not in sources.select_set(EScope.PRIVATE)
