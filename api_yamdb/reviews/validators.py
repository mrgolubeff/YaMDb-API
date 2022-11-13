from django.core.exceptions import ValidationError
from django.utils import timezone

MIN_YEAR = 1900


def year_validator(value):
    if value < MIN_YEAR or value > timezone.now().year:
        raise ValidationError(
            (f'{value} - неподходящий год'),
            params={'value': value},
        )
