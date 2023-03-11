from pymake.model.targets.custom_target import CustomTarget

class DocumentationTarget(CustomTarget):
    """
    Represents a target used to generate documentation for a project.
    """
    def __init__(self,
        target_name: str):
        """
        Initializes the target.
        @param target_name The name of the target.
        """
        super().__init__(target_name)
