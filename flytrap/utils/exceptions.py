class FlytrapError(Exception):
    """Custom exception class for Flytrap SDK errors."""
    def __init__(self, message: str, original_exception: Exception=None):
        """Initialize the custom error with a message and optional original exception."""
        super().__init__(message)
        self.original_exception = original_exception
