import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


# ----------------------------
# 1. Custom User Model
# ----------------------------
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(
        max_length=50,
        choices=[("admin", "Admin"), ("guest", "Guest")],
        default="guest",
    )

    def __str__(self):
        return self.username


# ----------------------------
# 2. Conversation Model
# ----------------------------
class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"


# ----------------------------
# 3. Message Model
# ----------------------------
class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(
        User, related_name="messages", on_delete=models.CASCADE
    )
    conversation = models.ForeignKey(
        Conversation, related_name="messages", on_delete=models.CASCADE
    )
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} in {self.conversation.id}"
