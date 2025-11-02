from typing import Any, Dict, List, Optional


class BaseAppException(Exception):
    """
    Base exception for all application exceptions.
    Enhanced with better error context and serialization.
    """

    def __init__(
        self,
        message: str,
        code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        cause: Optional[Exception] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code or self.__class__.__name__.upper()
        self.details = details or {}
        self.cause = cause

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.message}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(message='{self.message}', code='{self.code}')"

    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for serialization."""
        return {
            "type": self.__class__.__name__,
            "message": self.message,
            "code": self.code,
            "details": self.details,
        }


class AuthenticationError(BaseAppException):
    """Raised when authentication fails."""

    def __init__(
        self,
        message: str = "Authentication failed",
        code: str = "AUTH_FAILED",
        details: Optional[Dict[str, Any]] = None,
        cause: Optional[Exception] = None,
    ) -> None:
        super().__init__(message, code, details, cause)


class AuthorizationError(BaseAppException):
    """Raised when authorization fails."""

    def __init__(
        self,
        message: str = "Access denied",
        code: str = "ACCESS_DENIED",
        details: Optional[Dict[str, Any]] = None,
        cause: Optional[Exception] = None,
    ) -> None:
        super().__init__(message, code, details, cause)


class ValidationError(BaseAppException):
    """Raised when data validation fails."""

    def __init__(
        self,
        message: str = "Validation failed",
        code: str = "VALIDATION_ERROR",
        details: Optional[Dict[str, Any]] = None,
        errors: Optional[List[Dict[str, Any]]] = None,
        cause: Optional[Exception] = None,
    ) -> None:
        super().__init__(message, code, details, cause)
        self.errors = errors or []
        if self.errors and not details:
            self.details = {"validation_errors": self.errors}


class NotFoundError(BaseAppException):
    """Raised when a resource is not found."""

    def __init__(
        self,
        message: str = "Resource not found",
        code: str = "NOT_FOUND",
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        cause: Optional[Exception] = None,
    ) -> None:
        if not details and (resource_type or resource_id):
            details = {}
            if resource_type:
                details["resource_type"] = resource_type
            if resource_id:
                details["resource_id"] = resource_id

        super().__init__(message, code, details, cause)


class ConflictError(BaseAppException):
    """Raised when a resource conflict occurs."""

    def __init__(
        self,
        message: str = "Resource conflict",
        code: str = "CONFLICT",
        details: Optional[Dict[str, Any]] = None,
        cause: Optional[Exception] = None,
    ) -> None:
        super().__init__(message, code, details, cause)


class RateLimitError(BaseAppException):
    """Raised when rate limit is exceeded."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        code: str = "RATE_LIMIT_EXCEEDED",
        retry_after: int = 60,
        details: Optional[Dict[str, Any]] = None,
        cause: Optional[Exception] = None,
    ) -> None:
        if not details:
            details = {"retry_after": retry_after}
        super().__init__(message, code, details, cause)


class ServiceUnavailableError(BaseAppException):
    """Raised when a service is temporarily unavailable."""

    def __init__(
        self,
        message: str = "Service temporarily unavailable",
        code: str = "SERVICE_UNAVAILABLE",
        service_name: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        cause: Optional[Exception] = None,
    ) -> None:
        if not details and service_name:
            details = {"service": service_name}
        super().__init__(message, code, details, cause)
