from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.core import serializers
import json

from chat.decorators import user_can_join_room, verify_room
from chat.models import Message


JSONSerializer = serializers.get_serializer("json")


def index(request):
    return render(request, 'chat/index.html', {})


@verify_room(redirect_url='/chat/')
@user_can_join_room(redirect_url='/chat/')
@login_required(login_url='/chat/')
def room(request, room_name):
    messages_history = list(Message.get_chat_history(request.user, request.receiver))
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'receiver': request.receiver,
        'messages_history': messages_history
    })


@login_required(login_url='/chat/')
def home(request, user_id):
    return render(request, 'chat/home.html', {
        'receiver_name_json': mark_safe(json.dumps(user_id)),
    })
