from pymake.model.targets.docs.documentation_target import DocumentationTarget

class DoxygenTarget(DocumentationTarget):
    """
    Represents a target used to generate doxygen documentation for a project.
    """
    def __init__(self,
        target_name: str):
        """
        Initializes the target.
        @param target_name The name of the target.
        """
        super().__init__(target_name)
