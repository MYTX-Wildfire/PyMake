from pymake.model.project_scope import ProjectScope
from pymake.visitors.hierarchical.hierarchical_state import HierarchicalState
from pymake.visitors.visitor import IVisitor

class ProjectScopeVisitor(IVisitor[ProjectScope]):
    """
    Visitor that generates CMake code for a project scope.
    """
    def __init__(self, state: HierarchicalState):
        """
        Initializes the visitor.
        @param state Stores persistent state data gathered during the
            preprocessing phase. This data is used during the visit phase and
            should be considered immutable during that phase.
        """
        self._state = state


    def preprocess(self, node: ProjectScope) -> None:
        """
        Pre-processes the model object.
        @param node The model object to preprocess.
        """
        # Nothing to do
        pass


    def visit(self, node: ProjectScope) -> None:
        """
        Visits the model object.
        @param node The model object to visit.
        """
        generator = self._state.get_build_script_for_node(node).generator

        # Generate the project declaration
        with generator.open_method_block("project") as b:
            b.add_arguments(node.project_name)
            b.add_keyword_arguments(
                "LANGUAGES",
                *[l.value for l in node.project_languages]
            )

        # Generate the project's `all` target
        with generator.open_method_block("add_custom_target") as b:
            b.add_arguments(node.project_all_target_name, add_quotes=True)
            # Since the project's 'all' target doesn't build anything directly,
            #   add it to the `ALL` build target for completeness
            b.add_arguments("ALL")

        # Generate the project's `test` target
        with generator.open_method_block("add_custom_target") as b:
            b.add_arguments(node.project_test_target_name, add_quotes=True)
            # Since the project's 'test' target doesn't build anything directly,
            #   add it to the `ALL` build target for completeness
            b.add_arguments("ALL")

        # Set up a fixture that forces CMake to build the test targets before
        #   running the tests
        # CMake's default behavior is to not build the test targets before
        #   trying to run them. This behavior has been reported as a bug in
        #   2009, but CMake has yet to introduce a (dedicated) workaround
        #   for this behavior:
        #   https://gitlab.kitware.com/cmake/cmake/-/issues/8774
        # To get around this, use CMake fixtures as mentioned here:
        #   https://stackoverflow.com/a/56448477

        # Create and set up the test fixture target
        fixture_target_name = self._state.get_test_fixture_target_name(node)
        fixture_name = self._state.get_test_fixture_name(node)
        with generator.open_method_block("add_test") as b:
            b.add_arguments(fixture_target_name, add_quotes=True)
            b.add_arguments('"${CMAKE_COMMAND}"')
            b.add_arguments('--build "${CMAKE_BINARY_DIR}"')
            b.add_arguments('--config $<CONFIG>')
            b.add_arguments(f"--target {node.project_test_target_name}")
        with generator.open_method_block("set_tests_properties") as b:
            b.add_arguments(fixture_target_name, add_quotes=True)
            b.add_arguments("PROPERTIES")
            b.add_keyword_arguments(
                "FIXTURES_SETUP",
                fixture_name
            )

        # Generate add_subdirectory() calls for all target sets in the project
        for target_set in node.target_sets:
            with generator.open_method_block("add_subdirectory") as b:
                b.add_arguments(target_set.set_name)
