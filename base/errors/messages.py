from . import error_codes as errors


class ErrorMessageDict(dict):
    def get(self, key, default=None):
        default = default or 'Data validation failed.'
        return super().get(key, default)


error_messages = ErrorMessageDict({
    errors.DATA_VALIDATION_FAILED: "Data validation failed.",
    errors.RECORD_ALREADY_EXIST: "Record already exists.",
    errors.INVALID_UUID: "Invalid UUID.",
    errors.EMPTY_FILE: "The uploaded file cannot be empty.",
})


def message(error_code):
    return {
        "message": error_messages.get(error_code),
        "code": error_code
    }
