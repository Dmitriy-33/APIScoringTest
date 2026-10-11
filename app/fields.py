from __future__ import annotations

import datetime
from typing import Any, Optional


class FieldValidationError(Exception):
    pass


class Field:
    def __init__(self, required: bool = False, nullable: bool = False) -> None:
        self.required = required
        self.nullable = nullable
        self.name: Optional[str] = None

    def __set_name__(self, owner: type[Any], name: str) -> None:
        self.name = name

    def __get__(self, instance: Optional[Any], owner: type[Any]) -> Any:
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

    def __set__(self, instance: Any, value: Any) -> None:
        self._validate(value)
        instance.__dict__[self.name] = value

    def _validate(self, value: Any) -> None:
        if value is None:
            if self.required:
                raise FieldValidationError(f"Field '{self.name}' is required")
            return

        if value == "" or value == [] or value == {}:
            if not self.nullable:
                raise FieldValidationError(
                    f"Field '{self.name}' must not be empty"
                )
            return

        self._validate_type(value)

    def _validate_type(self, value: Any) -> None:
        pass


class CharField(Field):
    def _validate_type(self, value: Any) -> None:
        if not isinstance(value, str):
            raise FieldValidationError(
                f"Field '{self.name}' must be a string"
            )


class ArgumentsField(Field):
    def _validate_type(self, value: Any) -> None:
        if not isinstance(value, dict):
            raise FieldValidationError(
                f"Field '{self.name}' must be a dictionary"
            )


class EmailField(CharField):
    def _validate_type(self, value: Any) -> None:
        super()._validate_type(value)
        if "@" not in value:
            raise FieldValidationError(
                f"Field '{self.name}' must contain '@'"
            )


class PhoneField(Field):
    def _validate_type(self, value: Any) -> None:
        if isinstance(value, bool) or not isinstance(value, (str, int)):
            raise FieldValidationError(
                f"Field '{self.name}' must be a string or integer"
            )
        s = str(value)
        if len(s) != 11 or not s.startswith("7") or not s.isdigit():
            raise FieldValidationError(
                f"Field '{self.name}' must be 11 digits starting with 7"
            )


class DateField(Field):
    DATE_FORMAT = "%d.%m.%Y"

    def _validate_type(self, value: Any) -> None:
        if not isinstance(value, str):
            raise FieldValidationError(
                f"Field '{self.name}' must be a string in {self.DATE_FORMAT} format"
            )
        try:
            dt = datetime.datetime.strptime(value, self.DATE_FORMAT)
        except ValueError as exc:
            raise FieldValidationError(
                f"Field '{self.name}' must be a valid date in {self.DATE_FORMAT} format"
            ) from exc

        now = datetime.datetime.now()
        if dt > now:
            raise FieldValidationError(
                f"Field '{self.name}' cannot be in the future"
            )


class BirthDayField(DateField):
    MAX_AGE_YEARS = 70

    def _validate_type(self, value: Any) -> None:
        super()._validate_type(value)
        birthday = datetime.datetime.strptime(value, self.DATE_FORMAT)
        now = datetime.datetime.now()
        age_days = (now - birthday).days
        if age_days / 365.25 > self.MAX_AGE_YEARS:
            raise FieldValidationError(
                f"Field '{self.name}' must be within the last {self.MAX_AGE_YEARS} years"
            )


class GenderField(Field):
    ALLOWED_VALUES = {0, 1, 2}

    def _validate_type(self, value: Any) -> None:
        if isinstance(value, bool) or not isinstance(value, int):
            raise FieldValidationError(
                f"Field '{self.name}' must be an integer (0, 1 or 2)"
            )
        if value not in self.ALLOWED_VALUES:
            raise FieldValidationError(
                f"Field '{self.name}' must be 0, 1 or 2"
            )


class ClientIDsField(Field):
    def _validate_type(self, value: Any) -> None:
        if not isinstance(value, list):
            raise FieldValidationError(
                f"Field '{self.name}' must be a list of integers"
            )
        if len(value) == 0:
            raise FieldValidationError(
                f"Field '{self.name}' must not be empty"
            )
        for item in value:
            if isinstance(item, bool) or not isinstance(item, int):
                raise FieldValidationError(
                    f"Field '{self.name}' must contain only integers"
                )
