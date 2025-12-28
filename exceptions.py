"""Custom exceptions for user access control application."""


class UserException(Exception):
    """Base exception for user operations."""
    pass


class UserNotFoundError(UserException):
    """Raised when user doesn't exist."""
    def __init__(self, message: str = "User not found"):
        self.message = message
        super().__init__(self.message)


class DuplicateUserError(UserException):
    """Raised when user already exists."""
    def __init__(self, message: str = "User already exists"):
        self.message = message
        super().__init__(self.message)


class InvalidUserIDError(UserException):
    """Raised when user ID format is invalid."""
    def __init__(self, message: str = "Invalid user ID format"):
        self.message = message
        super().__init__(self.message)


class InvalidUserDataError(UserException):
    """Raised when user data is invalid."""
    def __init__(self, message: str = "Invalid user data"):
        self.message = message
        super().__init__(self.message)
