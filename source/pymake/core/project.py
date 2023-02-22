class Project:
    """
    Represents a single project scope in a PyMake project.
    """
    def __init__(self,
        project_name: str):
        """
        Initializes the project.
        """
        self._project_name = project_name


    @property
    def project_name(self) -> str:
        """
        Gets the name of the project.
        """
        return self._project_name
