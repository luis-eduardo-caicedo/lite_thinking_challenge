from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    is_admin = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name='+',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='+', 
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        if self.is_admin:
            self.is_staff = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
