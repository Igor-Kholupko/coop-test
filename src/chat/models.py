from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Message(models.Model):
    message = models.TextField()
    from_user = models.ForeignKey(
        User,
        models.DO_NOTHING,
        related_name='sent',
        related_query_name='sent'
    )
    to_user = models.ForeignKey(
        User,
        models.DO_NOTHING,
        related_name='received',
        related_query_name='received'
    )
    read = models.BooleanField()
