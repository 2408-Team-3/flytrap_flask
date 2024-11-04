class FlytrapError(Exception):
    """
    Custom exception class for Flytrap SDK errors.
    """
    def __init__(self, message: str, original_exception: Exception=None):
        """
        Initialize the custom error with a message and optional original exception.
        
        :param message: The error message to display.
        :param original_exception: The original exception that triggered this error (optional).
        """
        super().__init__(message)
        self.original_exception = original_exception
