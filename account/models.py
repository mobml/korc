from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid


class UserManager(BaseUserManager):
    """Custom user manager"""

    def create_user(self, email: str, password: str | None = None, **kwargs):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)

        if not password:
            raise ValueError("Password is required")

        user.save()
        return user

    def create_superuser(self, email: str, password: str | None = None, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault(
            "is_superuser", True
        )  # all control, this could change, but is good for now
        kwargs.setdefault("role", User.Role.OWNER)

        return self.create_user(email, password, **kwargs)


class User(AbstractUser):
    class Role(models.TextChoices):
        OWNER = "OWNER"
        ADMIN = "ADMIN"
        CASHIER = "CASHIER"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    username = None

    email = models.EmailField(unique=True)

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CASHIER,
    )

    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
