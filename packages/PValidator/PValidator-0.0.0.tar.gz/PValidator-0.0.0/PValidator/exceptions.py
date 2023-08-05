class _CodeExceptionSettings:
    _error_id = 1
    @staticmethod
    def error_incrementor():
        __class__._error_id += 1
        return __class__._error_id


class CodeException(BaseException):
    errors = {
        "required": {"id": _CodeExceptionSettings.error_incrementor(), "str": "field %s is required"},
        "missing": {"id": _CodeExceptionSettings.error_incrementor(), "str": "missing parameters"},
        "email": {"id": _CodeExceptionSettings.error_incrementor(), "str": "field %s is not an email"},
        "length": {"id": _CodeExceptionSettings.error_incrementor(), "str": "field %s must be %s chars. %s given"},
        "length_range": {"id": _CodeExceptionSettings.error_incrementor(),
                         "str": "field %s must be between %s and %s chars. %s given"},
        "length_min": {"id": _CodeExceptionSettings.error_incrementor(),
                       "str": "field %s must be at least %s chars. %s given"},
        "length_max": {"id": _CodeExceptionSettings.error_incrementor(),
                       "str": "field %s must be maximum %s chars. %s given"},
        "regex": {"id": _CodeExceptionSettings.error_incrementor(),
                       "str": "field %s has different pattern"},
        "email": {"id": _CodeExceptionSettings.error_incrementor(),
                  "str": "incorrect email address"},
    }


    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        placeholders = kwargs.get("placeholders", [])
        self._code: int = kwargs.get("id", None)
        self._str: str = kwargs.get("str", None)
        self._reference: str = kwargs.get("reference")
        self._apply_placeholders(placeholders)

    @property
    def get_reference(self):
        return self._reference

    def _apply_placeholders(self, placeholders):
        if placeholders:
            for and_replace_with in placeholders:
                and_replace_with = str(and_replace_with)
                find_this = "%s"
                occurrences = self._str.count(find_this)
                self._str = self._str.replace(find_this, and_replace_with, 1 if occurrences > 1 else occurrences)

    @property
    def get_code(self):
        return self._code

    @get_code.setter
    def get_code(self, c: int=0):
        self._code = c

    @property
    def message(self):
        return self._str


class LoopBreakerException(BaseException):
    pass
