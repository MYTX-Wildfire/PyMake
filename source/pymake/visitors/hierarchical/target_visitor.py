from abc import abstractmethod
from pathlib import Path
from pymake.common.sanitizer_flags import ESanitizerFlags
from pymake.common.scope import EScope
from pymake.core.scoped_sets import ScopedSets
from pymake.generators.cmake_generator import CMakeGenerator
from pymake.model.cmake_target_properties import CMakeTargetProperties
from pymake.model.cmake_config_target_properties import CMakeConfigTargetProperties
from pymake.model.targets.build.interface_target import InterfaceTarget
from pymake.model.targets.imported.imported_target import ImportedTarget
from pymake.model.targets.target import Target
from pymake.visitors.visitor import IVisitor
from pymake.tracing.caller_info import CallerInfo
from pymake.tracing.traced import Traced
from typing import Any, Dict, Generic, Iterable, List, Optional, Tuple, TypeVar

TargetType = TypeVar('TargetType', bound=Target)

class ITargetVisitor(IVisitor[TargetType], Generic[TargetType]):
    """
    Helper used to generate CMake code for targets.
    This class handles generation of CMake code that isn't specific to a
      particular target type. Generation of code specific to a target type is
      deferred to abstract methods.
    """
    def _generate(self,
        target: TargetType,
        generator: CMakeGenerator):
        """
        Generates the CMake code for the target.
        @param target The target to generate CMake code for.
        @param generator The CMake generator to add code to.
        """
        self._generate_target_declaration(target, generator)
        self._set_target_properties(target, target.properties, generator)
        for config in target.properties.configs:
            self._set_target_config_properties(
                target,
                config,
                target.properties.get_config_properties(config),
                generator
            )


    @abstractmethod
    def _generate_target_declaration(self,
        target: TargetType,
        generator: CMakeGenerator) -> None:
        """
        Generates the CMake code for the declaration of the target.
        @param target The target to generate CMake code for.
        @param generator The CMake generator to add code to.
        """
        raise NotImplementedError()


    def _set_target_properties(self,
        target: TargetType,
        properties: CMakeTargetProperties,
        generator: CMakeGenerator) -> None:
        """
        Generates CMake code that sets target properties.
        @param target The target to set properties on.
        @param properties The properties to set.
        @param generator The CMake generator to add code to.
        """
        # Determine which properties should be set on the target
        # Note that this process only needs to handle invalid properties for the
        #   target type; skipping unset properties is handled by the
        #   `_set_properties()` method.
        target_properties: Dict[str, Any] = {
            "CXX_CLANG_TIDY": properties.clang_tidy,
            "CXX_CLANG_TIDY_EXPORT_FIXES_DIR": properties.clang_tidy_export_fixes_dir,
            "CXX_COMPILER_LAUNCHER": properties.compiler_launcher,
            "CXX_CPP_CHECK": properties.cpp_check,
            "CXX_CPP_LINT": properties.cpp_lint,
            "CXX_INCLUDE_WHAT_YOU_USE": properties.iwyu,
            "CXX_LINKER_LAUNCHER": properties.linker_launcher,
            "CXX_VISIBILITY_PRESET": properties.visibility_preset,
            "ADDITIONAL_CLEAN_FILES": properties.additional_clean_files,
            "CXX_STANDARD": properties.cxx_standard,
            "CXX_STANDARD_REQUIRED": Traced(True),
            "EXCLUDE_FROM_ALL": properties.exclude_from_all,
            "BUILD_RPATH": properties.build_rpaths,
            "BUILD_RPATH_USE_ORIGIN": properties.build_rpath_use_origin,
            "INSTALL_RPATH": properties.install_rpaths,
            "INSTALL_RPATH_USE_LINK_PATH": properties.install_rpath_use_link_path,
            "IMPORTED": properties.imported,
            "IMPORTED_LIBNAME": properties.imported_name,
            "IMPORTED_IMPLIB_NAME": properties.imported_implib_name,
            "IMPORTED_LOCATION": properties.imported_location,
            "INTERPROCEDURAL_OPTIMIZATION": properties.interprocedural_optimization,
            "OUTPUT_NAME": properties.output_name,
            "POSITION_INDEPENDENT_CODE": properties.position_independent_code,
            "PREFIX": properties.prefix
        }

        # Remove properties that are invalid for the target type
        if isinstance(target, InterfaceTarget):
            target_properties.pop("CXX_STANDARD_REQUIRED", None)
        if not isinstance(target, ImportedTarget):
            target_properties.pop("IMPORTED", None)
            target_properties.pop("IMPORTED_LIBNAME", None)
            target_properties.pop("IMPORTED_IMPLIB_NAME", None)
            target_properties.pop("IMPORTED_LOCATION", None)

        # If a C++ standard isn't specified, don't mark it as required
        if not properties.cxx_standard.value:
            target_properties.pop("CXX_STANDARD_REQUIRED", None)

        self._set_properties(
            target,
            [(k, v) for k, v in target_properties.items()],
            generator
        )

        # Set compile definitions separately since they're stored as a tuple
        def compile_def_to_str(
            t: Traced[Tuple[str, Optional[str]]]) -> Traced[str]:
            if t.value[1] is None:
                return Traced(t.value[0], t.origin)
            else:
                return Traced(f"{t.value[0]}={t.value[1]}", t.origin)

        # Convert each entry into a string that can be passed to CMake
        compile_defs = properties.compile_definitions
        public_defs = [compile_def_to_str(t) for t in compile_defs.public]
        interface_defs = [compile_def_to_str(t) for t in compile_defs.interface]
        private_defs = [compile_def_to_str(t) for t in compile_defs.private]

        if compile_defs:
            with generator.open_method_block("target_compile_definitions") as b:
                b.add_arguments(target.target_name)

                # Add the definitions to the CMake code
                if public_defs:
                    b.add_keyword_arguments("PUBLIC", public_defs)
                if interface_defs:
                    b.add_keyword_arguments("INTERFACE", interface_defs)
                if private_defs:
                    b.add_keyword_arguments("PRIVATE", private_defs)

        # Set remaining scoped properties
        self._generate_compile_options(
            target,
            properties.compile_options,
            generator
        )
        self._generate_include_directories(
            target,
            properties.include_directories,
            generator
        )
        self._generate_link_libraries(
            target,
            target.properties.link_libraries,
            generator
        )
        self._generate_link_options(
            target,
            target.properties.link_options,
            generator
        )
        self._generate_sources(
            target,
            target.properties.sources,
            generator
        )

        # If sanitizers were requested, add them to the target
        if target.sanitizer_flags & ESanitizerFlags.ADDRESS:
            self._generate_asan_code(target, generator)
        if target.sanitizer_flags & ESanitizerFlags.MEMORY:
            self._generate_msan_code(target, generator)
        if target.sanitizer_flags & ESanitizerFlags.THREAD:
            self._generate_tsan_code(target, generator)
        if target.sanitizer_flags & ESanitizerFlags.UNDEFINED_BEHAVIOR:
            self._generate_ubsan_code(target, generator)
        if target.sanitizer_flags & ESanitizerFlags.LEAK:
            self._generate_lsan_code(target, generator)
        if target.sanitizer_flags & ESanitizerFlags.DATA_FLOW:
            self._generate_dfsan_code(target, generator)
        if target.sanitizer_flags & ESanitizerFlags.CONTROL_FLOW_INTEGRITY:
            self._generate_cfisan_code(target, generator)
        if target.sanitizer_flags & ESanitizerFlags.SAFE_STACK:
            self._generate_sssan_code(target, generator)

        # Generate the install command if the target is to be installed
        if properties.should_install.value:
            with generator.open_method_block("install") as b:
                # Write the location of the `install()` call in the PyMake build
                #   scripts above the name/location of the target
                if isinstance(target, ImportedTarget):
                    b.add_keyword_arguments(
                        "FILES",
                        Traced(
                            target.properties.imported_location,
                            target.properties.should_install.origin
                        )
                    )
                else:
                    b.add_keyword_arguments(
                        "TARGETS",
                        Traced(
                            target.target_name,
                            target.properties.should_install.origin
                        )
                    )

                if properties.install_path.value:
                    b.add_keyword_arguments(
                        "DESTINATION",
                        properties.install_path
                    )


    def _generate_compile_options(self,
        target: TargetType,
        options: ScopedSets[str],
        generator: CMakeGenerator):
        """
        Generates the target compile options code for the target.
        @param target The target to generate code for.
        @param options The options to add.
        @param generator The CMake generator to add code to.
        """
        self._set_scoped_properties(
            target,
            "target_compile_options",
            options,
            generator
        )


    def _generate_include_directories(self,
        target: TargetType,
        includes: ScopedSets[Path],
        generator: CMakeGenerator):
        """
        Generates the target include directories code for the target.
        @param target The target to generate code for.
        @param includes The include directories to add.
        @param generator The CMake generator to add code to.
        """
        self._set_scoped_properties(
            target,
            "target_include_directories",
            includes,
            generator
        )


    def _generate_link_libraries(self,
        target: TargetType,
        libraries: ScopedSets[str],
        generator: CMakeGenerator):
        """
        Generates the target link libraries code for the target.
        @param target The target to generate code for.
        @param libraries The libraries to link to.
        @param generator The CMake generator to add code to.
        """
        self._set_scoped_properties(
            target,
            "target_link_libraries",
            libraries,
            generator
        )


    def _generate_link_options(self,
        target: TargetType,
        options: ScopedSets[str],
        generator: CMakeGenerator):
        """
        Generates the target link options code for the target.
        @param target The target to generate code for.
        @param options The options to add.
        @param generator The CMake generator to add code to.
        """
        self._set_scoped_properties(
            target,
            "target_link_options",
            options,
            generator
        )


    def _generate_sources(self,
        target: TargetType,
        sources: ScopedSets[Path],
        generator: CMakeGenerator):
        """
        Generates the target sources code for the target.
        @param target The target to generate code for.
        @param sources The sources to add.
        @param generator The CMake generator to add code to.
        """
        self._set_scoped_properties(
            target,
            "target_sources",
            sources,
            generator
        )


    def _set_target_config_properties(self,
        target: TargetType,
        config: str,
        properties: CMakeConfigTargetProperties,
        generator: CMakeGenerator) -> None:
        """
        Generates CMake code that sets target properties for a specific config.
        @param target The target to set properties on.
        @param config The config to set properties for.
        @param properties The properties to set.
        @param generator The CMake generator to add code to.
        """
        self._set_properties(
            target,
            [
                (f"IMPORTED_LIBNAME_{config}", properties.imported_library_name),
                (f"IMPORTED_IMPLIB_{config}", properties.imported_implib_name),
                (f"IMPORTED_LOCATION_{config}", properties.imported_location)
            ],
            generator
        )


    def _set_properties(self,
        target: TargetType,
        properties: Iterable[Tuple[str, Traced[Optional[Any]] | Iterable[Traced[Any]]]],
        generator: CMakeGenerator) -> None:
        """
        Generates CMake code that sets target properties.
        If no properties should be set, this method will not generate any CMake
          code.
        @param target The target to set properties on.
        @param properties The properties to set. Each element returned by the
          iterable should be a tuple of the property name and the property
          value. Property values may also be a list of individually traced
          values.
        @param generator The CMake generator to add code to.
        """
        # Get only the properties that have a value
        def has_value(p: Traced[Optional[Any]] | Iterable[Traced[Any]]) -> bool:
            if isinstance(p, Traced):
                return bool(p.value)
            else:
                return len(list(p)) > 0
        set_properties = list(filter(lambda p: has_value(p[1]), properties))

        # If no properties have a value set, don't generate any code
        if not set_properties:
            return

        # Generate the call to set the properties
        with generator.open_method_block("set_target_properties") as b:
            b.add_arguments(target.target_name)
            b.add_arguments("PROPERTIES")
            for property_name, value in set_properties:
                if isinstance(value, Traced):
                    b.add_keyword_arguments(property_name, value)
                else:
                    b.add_keyword_arguments(property_name, *value)


    def _set_scoped_properties(self,
        target: TargetType,
        setter_function: str,
        scoped_set: ScopedSets[Any],
        generator: CMakeGenerator) -> None:
        """
        Generates CMake code that sets scoped properties.
        @param target The target to set properties on.
        @param setter_function The CMake function to use to set the properties.
        @param scoped_set The scoped set of properties to set.
        @param generator The CMake generator to add code to.
        """
        if not scoped_set:
            return

        with generator.open_method_block(setter_function) as b:
            b.add_arguments(target.target_name)

            # Skip scopes that have no values
            if scoped_set.public:
                b.add_keyword_arguments("PUBLIC", *scoped_set.public)
            if scoped_set.interface:
                b.add_keyword_arguments("INTERFACE", *scoped_set.interface)
            if scoped_set.private:
                b.add_keyword_arguments("PRIVATE", *scoped_set.private)


    def _generate_asan_code(self,
        target: TargetType,
        generator: CMakeGenerator) -> None:
        """
        Generates CMake code that adds address sanitizer to a target.
        @param target The target to add address sanitizer to.
        @param generator The CMake generator to add code to.
        """
        self._generate_sanitizer_flags(
            target,
            target.origin,
            clang_flags=["-fsanitize=address"],
            gcc_flags=["-fsanitize=address"],
            msvc_flags=["/fsanitize=address"],
            generator=generator
        )


    def _generate_msan_code(self,
        target: TargetType,
        generator: CMakeGenerator) -> None:
        """
        Generates CMake code that adds address sanitizer to a target.
        @param target The target to add address sanitizer to.
        @param generator The CMake generator to add code to.
        """


    def _generate_tsan_code(self,
        target: TargetType,
        generator: CMakeGenerator) -> None:
        """
        Generates CMake code that adds address sanitizer to a target.
        @param target The target to add address sanitizer to.
        @param generator The CMake generator to add code to.
        """


    def _generate_lsan_code(self,
        target: TargetType,
        generator: CMakeGenerator) -> None:
        """
        Generates CMake code that adds address sanitizer to a target.
        @param target The target to add address sanitizer to.
        @param generator The CMake generator to add code to.
        """


    def _generate_ubsan_code(self,
        target: TargetType,
        generator: CMakeGenerator) -> None:
        """
        Generates CMake code that adds address sanitizer to a target.
        @param target The target to add address sanitizer to.
        @param generator The CMake generator to add code to.
        """


    def _generate_dfsan_code(self,
        target: TargetType,
        generator: CMakeGenerator) -> None:
        """
        Generates CMake code that adds address sanitizer to a target.
        @param target The target to add address sanitizer to.
        @param generator The CMake generator to add code to.
        """


    def _generate_cfisan_code(self,
        target: TargetType,
        generator: CMakeGenerator) -> None:
        """
        Generates CMake code that adds address sanitizer to a target.
        @param target The target to add address sanitizer to.
        @param generator The CMake generator to add code to.
        """


    def _generate_sssan_code(self,
        target: TargetType,
        generator: CMakeGenerator) -> None:
        """
        Generates CMake code that adds address sanitizer to a target.
        @param target The target to add address sanitizer to.
        @param generator The CMake generator to add code to.
        """


    def _generate_sanitizer_flags(self,
        target: Target,
        origin: CallerInfo,
        clang_flags: List[str],
        gcc_flags: List[str],
        msvc_flags: List[str],
        generator: CMakeGenerator) -> None:
        """
        Generates CMake code that adds sanitizer flags to a target.
        @param target The target to add sanitizer flags to.
        @param origin The location where the sanitizer flag was set.
        @param clang_flags The flags to use when building with Clang.
        @param gcc_flags The flags to use when building with GCC.
        @param msvc_flags The flags to use when building with MSVC.
        @param generator The CMake generator to add code to.
        """
        # Enable address sanitizer when building with Clang
        self._generate_compiler_specific_sanitizer_flags(
            target,
            origin,
            "Clang",
            clang_flags,
            generator
        )
        self._generate_compiler_specific_sanitizer_flags(
            target,
            origin,
            "GNU",
            gcc_flags,
            generator
        )
        self._generate_compiler_specific_sanitizer_flags(
            target,
            origin,
            "MSVC",
            msvc_flags,
            generator
        )


    def _generate_compiler_specific_sanitizer_flags(self,
        target: Target,
        origin: CallerInfo,
        compiler: str,
        flags: List[str],
        generator: CMakeGenerator) -> None:
        """
        Generates CMake code that adds sanitizer flags to a target.
        @param target The target to add sanitizer flags to.
        @param origin The location where the sanitizer flag was set.
        @param compiler The compiler to generate flags for.
        @param flags The flags to use when building with the specified compiler.
        @param generator The CMake generator to add code to.
        """
        # Determine what scope to use for the address sanitizer flags
        scope = EScope.PUBLIC
        if isinstance(target, ImportedTarget):
            scope = EScope.INTERFACE
        scope = scope.value

        # Generate the CMake code
        generator.open_if_block(
            f"${{CMAKE_CXX_COMPILER_ID}} MATCHES \"{compiler}\""
        )
        with generator.open_method_block("target_compile_options") as b:
            b.add_arguments(target.target_name)
            b.add_keyword_arguments(
                scope,
                *[Traced(f, origin) for f in flags],
                add_quotes=True
            )
        with generator.open_method_block("target_link_options") as b:
            b.add_arguments(target.target_name)
            b.add_keyword_arguments(
                scope,
                *[Traced(f, origin) for f in flags],
                add_quotes=True
            )
        generator.close_if_block()
