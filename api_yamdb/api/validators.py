from rest_framework.exceptions import ValidationError
from users.models import User


def validate_username(value):
    if value == "me":
        raise ValidationError("Имя недоступно!")
    elif User.objects.filter(username=value).exists():
        raise ValidationError(
            "Пользователь с таким именем уже существует"
        )
    return value


def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError(
            "Почта уже использовалась для регистрации"
        )
