from django.contrib.auth.models import AbstractUser
from django.db import models

from .utils import ROLE_CHOICE, ROLE_TERMS


class User(AbstractUser):
    email = models.EmailField(
        verbose_name="Адрес электронной почты",
        unique=True,
    )
    username = models.CharField(
        verbose_name="Имя пользователя", max_length=150, unique=True
    )
    role = models.CharField(
        max_length=25,
        default=ROLE_TERMS["user"],
        choices=ROLE_CHOICE
    )
    bio = models.TextField(max_length=4096, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["username", "email"], name="unique_username_email"
            )
        ]

    def is_admin(self):
        return self.role == ROLE_TERMS["admin"]

    def is_moderator(self):
        return self.role == ROLE_TERMS["moderator"]
