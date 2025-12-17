import logging

from rest_framework import status
from rest_framework.exceptions import APIException

from .error_codes import NO_CODE, DATA_VALIDATION_FAILED
from .messages import error_messages

logger = logging.getLogger(__name__)

__all__ = [
    'TaskException',
    'NotificationException',
    'PMDataIntegrityException',
    'PMValidationError'
]


class TaskException(Exception):
    pass


class NotificationException(Exception):
    pass


class InsufficientStock(Exception):
    pass


class PMDataIntegrityException(Exception):
    pass


class PMValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    app_code = NO_CODE

    @property
    def _error_message(self):
        if self.app_code == DATA_VALIDATION_FAILED:
            return self.detail  # send default message
        return error_messages.get(self.app_code)

    def __init__(self, detail=None, code=None, app_code=None):
        super().__init__(detail, code)
        self.app_code = app_code
        if not app_code:
            logger.error(f"Validation Error: {self.detail}")
        self.detail = {
            "message": self._error_message if app_code else "Data validation failed.",
            "code": app_code
        }
