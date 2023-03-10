from pathlib import Path
from pymake.common.project_language import EProjectLanguage
from pymake.core.build_script_set import BuildScriptSet
from pymake.core.project import Project
from pymake.targets.executable_target import ExecutableTarget
from pymake.targets.shared_library_target import SharedLibraryTarget
from pymake.targets.static_library_target import StaticLibraryTarget
from pymake.targets.target import ITarget
from pymake.tracing.null_caller_info_formatter import NullCallerInfoFormatter
import pytest
from typing import Callable, Optional

class TestProject:
    build_scripts_set = BuildScriptSet(
        Path("/source"),
        Path("/generated"),
        NullCallerInfoFormatter()
    )

    def test_project_name_matches_ctor_arg(self):
        project_name = "foo"
        project = Project(
            self.build_scripts_set,
            project_name,
            EProjectLanguage.Cpp
        )
        assert project.project_name == project_name


    def test_project_language_matches_ctor_arg(self):
        project_language = EProjectLanguage.Cpp
        project = Project(
            self.build_scripts_set,
            "foo",
            project_language
        )
        assert project.project_languages
        assert project_language in project.project_languages


    def test_creating_project_generates_cmake_code(self):
        project = Project(
            self.build_scripts_set,
            "foo",
            EProjectLanguage.Cpp
        )
        assert self.build_scripts_set

        build_script = self.build_scripts_set.get_or_add_build_script()
        code = build_script.generator.generate()
        assert code
        assert "project" in code
        assert project.project_name in code


    def test_add_executable_returns_executable_with_given_name(self):
        project = Project(
            self.build_scripts_set,
            "foo",
            EProjectLanguage.Cpp
        )
        executable_name = "bar"
        executable = project.add_executable(executable_name)
        assert executable
        assert executable.target_name == executable_name


    def test_add_duplicate_executable_allowed_if_origin_is_identical(self):
        project = Project(
            self.build_scripts_set,
            "foo",
            EProjectLanguage.Cpp
        )

        # This would normally be handled by the `ICMake` instance that constructs
        #   the project.
        executable_name = "bar"
        on_target_added: Callable[[ITarget], Optional[ITarget]] = lambda x: x
        project.on_target_added = on_target_added

        # This should not throw despite `on_target_added` returning an object
        project.add_executable(executable_name)


    def test_add_executable_throws_if_duplicate_name(self):
        project = Project(
            self.build_scripts_set,
            "foo",
            EProjectLanguage.Cpp
        )

        # This would normally be handled by the `ICMake` instance that constructs
        #   the project.
        executable_name = "bar"
        target = ExecutableTarget(self.build_scripts_set, executable_name)
        on_target_added: Callable[[ITarget], Optional[ITarget]] = lambda x: target
        project.on_target_added = on_target_added

        with pytest.raises(ValueError):
            project.add_executable(executable_name)


    def test_add_shared_library_returns_shared_library_with_given_name(self):
        project = Project(
            self.build_scripts_set,
            "foo",
            EProjectLanguage.Cpp
        )
        shared_library_name = "bar"
        shared_library = project.add_shared_library(shared_library_name)
        assert shared_library
        assert shared_library.target_name == shared_library_name


    def test_add_duplicate_shared_library_allowed_if_origin_is_identical(self):
        project = Project(
            self.build_scripts_set,
            "foo",
            EProjectLanguage.Cpp
        )

        # This would normally be handled by the `ICMake` instance that constructs
        #   the project.
        shared_library_name = "bar"
        on_target_added: Callable[[ITarget], Optional[ITarget]] = lambda x: x
        project.on_target_added = on_target_added

        # This should not throw despite `on_target_added` returning an object
        project.add_shared_library(shared_library_name)


    def test_add_shared_library_throws_if_duplicate_name(self):
        project = Project(
            self.build_scripts_set,
            "foo",
            EProjectLanguage.Cpp
        )

        # This would normally be handled by the `ICMake` instance that constructs
        #   the project.
        shared_library_name = "bar"
        target = SharedLibraryTarget(self.build_scripts_set, shared_library_name)
        on_target_added: Callable[[ITarget], Optional[ITarget]] = lambda x: target
        project.on_target_added = on_target_added

        with pytest.raises(ValueError):
            project.add_shared_library(shared_library_name)


    def test_add_static_library_returns_static_library_with_given_name(self):
        project = Project(
            self.build_scripts_set,
            "foo",
            EProjectLanguage.Cpp
        )
        static_library_name = "bar"
        static_library = project.add_static_library(static_library_name)
        assert static_library
        assert static_library.target_name == static_library_name


    def test_add_duplicate_static_library_allowed_if_origin_is_identical(self):
        project = Project(
            self.build_scripts_set,
            "foo",
            EProjectLanguage.Cpp
        )

        # This would normally be handled by the `ICMake` instance that constructs
        #   the project.
        static_library_name = "bar"
        on_target_added: Callable[[ITarget], Optional[ITarget]] = lambda x: x
        project.on_target_added = on_target_added

        # This should not throw despite `on_target_added` returning an object
        project.add_static_library(static_library_name)


    def test_add_static_library_throws_if_duplicate_name(self):
        project = Project(
            self.build_scripts_set,
            "foo",
            EProjectLanguage.Cpp
        )

        # This would normally be handled by the `ICMake` instance that constructs
        #   the project.
        static_library_name = "bar"
        target = StaticLibraryTarget(self.build_scripts_set, static_library_name)
        on_target_added: Callable[[ITarget], Optional[ITarget]] = lambda x: target
        project.on_target_added = on_target_added

        with pytest.raises(ValueError):
            project.add_static_library(static_library_name)
