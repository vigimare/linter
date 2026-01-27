from enum import Enum
from typing import override


class LinterErrorType(Enum):
    FILE_NOT_FOUND = "File not found"
    VALIDATION_ERROR = "Validation error"
    SYNTAX_ERROR = "Syntax error"
    CONFIG_ERROR = "Configuration error"
    UNKNOWN_ERROR = "Unknown error"
    SCHEMA_ERROR = "XSD Schema could not be parsed"
    BASE64_ERROR = "BASE64 encoding error"
    NOT_A_DIRECTORY = "The provided directory for XSD path was not found"


class LinterSuccessType(Enum):
    BASE_MESSAGE = "Linting was successful"
    DOCUMENT_SUCCESS = "All embedded documents are valid"


class LinterError(Exception):
    def __init__(self, error_type: LinterErrorType, original_exception: Exception | None = None):
        self.error_type: LinterErrorType = error_type
        self.original_exception: Exception | None = original_exception
        message = error_type.value
        if original_exception:
            reason = getattr(original_exception, "reason", None)
            if reason:
                message += f": {reason}"
            else:
                message += f": {str(original_exception)}"
        super().__init__(message)


class LinterSuccess:
    def __init__(self, success_type: LinterSuccessType, extra_info: str | None = None):
        self.success_type: LinterSuccessType = success_type
        self.message: str = success_type.value
        self.extra_info: str | None = extra_info if extra_info is not None else ""

    @override
    def __str__(self):
        return f"{self.message} {self.extra_info}"
