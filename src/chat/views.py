from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
import json

from chat.decorators import user_can_join_room, verify_room


def index(request):
    return render(request, 'chat/index.html', {})


@verify_room(redirect_url='/chat/')
@user_can_join_room(redirect_url='/chat/')
@login_required(login_url='/chat/')
def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'receiver_name_json': mark_safe(json.dumps(room_name.split('-')[0])),
    })


@login_required(login_url='/chat/')
def home(request, user_id):
    return render(request, 'chat/home.html', {
        'receiver_name_json': mark_safe(json.dumps(user_id)),
    })
