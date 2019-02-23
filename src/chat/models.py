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
    read = models.BooleanField(
        default=False
    )
    time = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )

    @classmethod
    def get_chat_history(cls, user_one, user_two, depth=None):
        if type(user_one) == User:
            user_one = user_one.id
        if type(user_two) == User:
            user_two = user_two.id
        users_id_list = [user_one, user_two]
        return cls.objects.filter(from_user_id__in=users_id_list, to_user_id__in=users_id_list).order_by('id')
