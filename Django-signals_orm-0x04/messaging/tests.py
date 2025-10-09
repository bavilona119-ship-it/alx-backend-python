from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class MessageSignalTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='alice', password='test123')
        self.receiver = User.objects.create_user(username='bob', password='test123')

    def test_notification_created_on_new_message(self):
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello Bob!"
        )
        notification = Notification.objects.filter(user=self.receiver, message=message).first()

        self.assertIsNotNone(notification)
        self.assertEqual(notification.text, f"New message from {self.sender.username}")
