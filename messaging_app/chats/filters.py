# chats/filters.py
import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    sent_after = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr="gte")
    sent_before = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr="lte")
    sender = django_filters.CharFilter(field_name="sender__user_id")  # ou email selon ton modèle

    class Meta:
        model = Message
        fields = ["sender", "sent_after", "sent_before"]
