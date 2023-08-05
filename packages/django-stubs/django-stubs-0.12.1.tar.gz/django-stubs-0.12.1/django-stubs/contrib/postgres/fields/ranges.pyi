from typing import Any

from django.db import models

from psycopg2.extras import DateRange, DateTimeTZRange, NumericRange  # type: ignore

class RangeField(models.Field):
    empty_strings_allowed: bool = ...
    base_field: Any = ...
    range_type: Any = ...
    def get_prep_value(self, value: Any): ...
    def to_python(self, value: Any): ...
    def value_to_string(self, obj: Any): ...

class IntegerRangeField(RangeField):
    def __get__(self, instance, owner) -> NumericRange: ...

class BigIntegerRangeField(RangeField):
    def __get__(self, instance, owner) -> NumericRange: ...

class FloatRangeField(RangeField):
    def __get__(self, instance, owner) -> NumericRange: ...

class DateTimeRangeField(RangeField):
    def __get__(self, instance, owner) -> DateTimeTZRange: ...

class DateRangeField(RangeField):
    def __get__(self, instance, owner) -> DateRange: ...
