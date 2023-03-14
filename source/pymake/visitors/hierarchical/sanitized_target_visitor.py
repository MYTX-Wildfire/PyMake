from pathlib import Path
from pymake.common.scope import EScope
from pymake.common.target_type import ETargetType
from pymake.core.scoped_sets import ScopedSets
from pymake.generators.cmake_generator import CMakeGenerator
from pymake.model.cmake_target_properties import CMakeTargetProperties
from pymake.model.cmake_config_target_properties import CMakeConfigTargetProperties
from pymake.model.targets.build.build_target import BuildTarget
from pymake.model.targets.build.interface_target import InterfaceTarget
from pymake.model.targets.build.sanitized_target import SanitizedTarget
from pymake.model.targets.imported.imported_target import ImportedTarget
from pymake.tracing.traced import Traced
from pymake.visitors.hierarchical.hierarchical_state import HierarchicalState
from pymake.visitors.hierarchical.target_visitor import ITargetVisitor
from typing import Optional, Tuple

class SanitizedTargetVisitor(ITargetVisitor[SanitizedTarget]):
    """
    Visitor that generates CMake code for a sanitized target.
    """
    def __init__(self, state: HierarchicalState):
        """
        Initializes the visitor.
        @param state Stores persistent state data gathered during the
            preprocessing phase. This data is used during the visit phase and
            should be considered immutable during that phase.
        """
        self._state = state


    def preprocess(self, node: SanitizedTarget) -> None:
        """
        Pre-processes the model object.
        @param node The model object to preprocess.
        """
        # Nothing to do
        pass


    def visit(self, node: SanitizedTarget) -> None:
        """
        Visits the model object.
        @param node The model object to visit.
        """
        generator = self._state.get_build_script_for_node(node).generator
        self._generate(node, generator)


    def _generate_target_declaration(self,
        target: SanitizedTarget,
        generator: CMakeGenerator) -> None:
        """
        Generates the CMake code for the declaration of the target.
        @param target The target to generate CMake code for.
        @param generator The CMake generator to add code to.
        """
        # Sanitized targets may wrap any other build target type. Check its
        #   wrapped target's type and generate the correct declaration
        if target.target_type == ETargetType.EXECUTABLE:
            with generator.open_method_block("add_executable") as b:
                b.add_arguments(
                    Traced(target.target_name, target.origin)
                )
        elif target.target_type == ETargetType.SHARED:
            with generator.open_method_block("add_library") as b:
                b.add_arguments(
                    Traced(target.target_name, target.origin),
                    "SHARED"
                )
        elif target.target_type == ETargetType.STATIC:
            with generator.open_method_block("add_library") as b:
                b.add_arguments(
                    Traced(target.target_name, target.origin),
                    "STATIC"
                )
        else:
            raise ValueError("Unsupported target type: {target.target_type}")


    def _generate_target_properties(self,
        target: SanitizedTarget,
        properties: CMakeTargetProperties,
        generator: CMakeGenerator):
        """
        Generates CMake code that sets each of the target's properties.
        @param target The target to generate code for.
        @param properties The properties to set.
        @param generator The CMake generator to add code to.
        """
        super()._generate_target_properties(
            target,
            target.wrapped_target.properties,
            generator
        )


    def _generate_target_config_properties(self,
        target: SanitizedTarget,
        config: str,
        properties: CMakeConfigTargetProperties,
        generator: CMakeGenerator):
        """
        Generates CMake code that sets config-specific target properties.
        @param target The target to generate code for.
        @param config The config to generate code for.
        @param properties The properties to set.
        @param generator The CMake generator to add code to.
        """
        super()._generate_target_config_properties(
            target,
            config,
            target.wrapped_target.properties.get_config_properties(config),
            generator
        )


    def _generate_compile_definitions(self,
        target: SanitizedTarget,
        defs: ScopedSets[Tuple[str, Optional[str]]],
        generator: CMakeGenerator):
        """
        Generates the target compile definitions code for the target.
        @param target The target to generate code for.
        @param defs The definitions to add.
        @param generator The CMake generator to add code to.
        """
        super()._generate_compile_definitions(
            target,
            target.wrapped_target.properties.compile_definitions,
            generator
        )


    def _generate_compile_options(self,
        target: SanitizedTarget,
        options: ScopedSets[str],
        generator: CMakeGenerator):
        """
        Generates the target compile options code for the target.
        @param target The target to generate code for.
        @param options The options to add.
        @param generator The CMake generator to add code to.
        """
        super()._generate_compile_options(
            target,
            target.wrapped_target.properties.compile_options,
            generator
        )


    def _generate_include_directories(self,
        target: SanitizedTarget,
        includes: ScopedSets[Path],
        generator: CMakeGenerator):
        """
        Generates the target include directories code for the target.
        @param target The target to generate code for.
        @param includes The include directories to add.
        @param generator The CMake generator to add code to.
        """
        super()._generate_include_directories(
            target,
            target.wrapped_target.properties.include_directories,
            generator
        )


    def _generate_link_libraries(self,
        target: SanitizedTarget,
        libraries: ScopedSets[str],
        generator: CMakeGenerator):
        """
        Generates the target link libraries code for the target.
        @param target The target to generate code for.
        @param libraries The libraries to link to.
        @param generator The CMake generator to add code to.
        """
        # Process the libraries from the wrapped target, not the sanitized
        #   target wrapper
        libraries = target.wrapped_target.properties.link_libraries

        # For each library that this target links to, look up its target set.
        #   Each library that the original wrapped target links to must be
        #   replaced with the sanitized version of the library.
        sanitized_libraries: ScopedSets[str] = ScopedSets()
        for scope in EScope:
            for library in libraries.select_set(scope):
                # Look up the target with the given name
                linked_target = self._state.get_target_by_name(
                    library.value
                )

                # TODO: Handle the common interface target
                if isinstance(linked_target, InterfaceTarget):
                    continue

                # These are the only types of targets that can be linked to and
                #    have a sanitized variant
                assert isinstance(linked_target, (
                    BuildTarget,
                    ImportedTarget,
                    SanitizedTarget
                ))

                # Look up the target set for the library
                library_target_set = self._state.get_target_set_by_target(
                    linked_target
                )

                # Look up the sanitized target for the library
                # TODO: Catch a thrown exception and add more information to
                #   the exception message before re-throwing it
                sanitized_target = library_target_set.find_sanitized_target(
                    target.sanitizer_flags,
                    linked_target.target_type
                )
                sanitized_libraries.select_set(scope).add(
                    sanitized_target.target_name,
                    library.origin
                )

        # Generate the link libraries code
        super()._generate_link_libraries(
            target,
            sanitized_libraries,
            generator
        )


    def _generate_link_options(self,
        target: SanitizedTarget,
        options: ScopedSets[str],
        generator: CMakeGenerator):
        """
        Generates the target link options code for the target.
        @param target The target to generate code for.
        @param options The options to add.
        @param generator The CMake generator to add code to.
        """
        super()._generate_link_options(
            target,
            target.wrapped_target.properties.link_options,
            generator
        )


    def _generate_sources(self,
        target: SanitizedTarget,
        sources: ScopedSets[Path],
        generator: CMakeGenerator):
        """
        Generates the target sources code for the target.
        @param target The target to generate code for.
        @param sources The sources to add.
        @param generator The CMake generator to add code to.
        """
        super()._generate_sources(
            target,
            target.wrapped_target.properties.sources,
            generator
        )


    def _generate_install(self,
        target: SanitizedTarget,
        is_imported: bool,
        install_path: Traced[Optional[Path]],
        generator: CMakeGenerator) -> None:
        """
        Generates CMake code that installs a target.
        @param target The target to install.
        @param is_imported Whether to use the imported location of the target
          when installing.
        @param install_path The path to install the target to. If this is none,
          the default CMake install path for the target type will be used.
        @param generator The CMake generator to add code to.
        """
        super()._generate_install(
            target,
            isinstance(target.wrapped_target, ImportedTarget),
            target.properties.install_path,
            generator
        )
