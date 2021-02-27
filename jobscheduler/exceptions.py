class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class ValidationError(Error):
    """Exception raised for errors during validation.

    Attributes:
        validation -- validation being performed
        message -- explanation of the error
    """

    def __init__(self, validation, message):
        self.validation = validation
        self.message = message