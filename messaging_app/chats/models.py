# messaging_app/chats/models.py

import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom User model extending AbstractUser.
    Built-in fields already included from AbstractUser:
      - password
      - first_name
      - last_name
      - email
    """

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    # email is already in AbstractUser, but we redefine for uniqueness enforcement
    email = models.EmailField(unique=True, null=False, blank=False)

    phone_number = models.CharField(max_length=20, null=True, blank=True)

    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')

    created_at = models.DateTimeField(auto_now_add=True)

    # remove username, use email instead
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']

    class Meta:
        indexes = [
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
