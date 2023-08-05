import re
from collections import defaultdict
from .exceptions import (
    CodeException, LoopBreakerException
)


class Validator:
    def __init__(self, ref):
        self._reference = ref
        self._field_value = ""
        self._field_name = ""
        self._single_error = False
        self._rule_params = None
        self.errors = 0
        self.failed = defaultdict(dict)

    @property
    def field_name(self):
        return self._field_name

    @field_name.setter
    def field_name(self, fn):
        self._field_name = fn

    @property
    def field_value(self):
        return self._field_value

    @field_value.setter
    def field_value(self, fv):
        self._field_value = fv

    def raise_(self, error_key, *placeholders):
        raise CodeException(reference=self.field_name, placeholders=placeholders, **CodeException.errors[error_key])

    def _require(self, *args):
        if not getattr(self._reference, self.field_name) or not self.field_value:
            self.raise_("required", self.field_name)

    def _regex(self, *args):
        if not len(args):
            raise Exception("missing pattern")

        pattern = args[0]
        if not re.match(pattern, self.field_value):
            self.raise_("regex", self.field_name)

    def _email(self, *args):
        try:
            self._regex(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        except:
            self.raise_("email", self.field_name)

    def _length(self, *args):
        from_, to_, equal = ("", "", "")
        total_args = len(args)
        value_length = len(self._field_value)

        if total_args == 3:
            equal = args[0]
            from_ = args[1]
            to_ = args[2]
        elif total_args == 2:
            equal = args[0]
            from_ = args[1]
        elif total_args == 1:
            equal = args[0]
        else:
            raise Exception("length validation Argument ERROR!")
        equal, from_, to_ = str(equal), str(from_), str(to_)

        if equal and value_length != equal:
            self.raise_("length", self.field_name, equal, value_length)

        if (from_ and to_) and not int(from_) <= value_length <= int(to_):
            self.raise_("length_range", self.field_name, from_, to_, value_length)
        elif from_ and value_length < int(from_):
            self.raise_("length_min", self.field_name, from_, value_length)
        elif to_ and value_length > int(to_):
            self.raise_("length_max", self.field_name, to_, value_length)

    def single(self):
        self._single_error = True
        return self

    def get_failed(self) -> dict:
        return self.failed

    def validate(self, **rules):
        try:
            for field, rule in rules.items():
                rule = str(rule)
                rule = rule[:-1] if rule.endswith("|") else rule
                self.field_name = field
                self.field_value = getattr(self._reference, field)

                if hasattr(self._reference, self.field_name):
                    for rule_method in rule.split("|"):
                        _rule_method, *args = rule_method.split(":")
                        exists_method = f"_{_rule_method}"
                        method = getattr(self, exists_method, None)
                        if callable(method):
                            try:
                                method(*args)
                            except CodeException as Exc:
                                self.errors += 1
                                self.failed[self._field_name][_rule_method] = Exc
                                if self._single_error:
                                    raise LoopBreakerException()
                        else:
                            raise Exception("validation {} not supported".format(_rule_method))
        except LoopBreakerException:
            pass

        return self


Validator = Validator