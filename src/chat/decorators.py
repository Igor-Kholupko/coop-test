from functools import wraps
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect


User = get_user_model()


from django.contrib.auth.models import User


def user_can_join_room(redirect_url=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, room_name, *args, **kwargs):
            return view_func(request, room_name, *args, **kwargs)
        return _wrapped_view
    return decorator


def verify_room(redirect_url=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, room_name, *args, **kwargs):
            splited_rn = room_name.split('-')
            if len(splited_rn) \
                    or User.objects.filter(id__in=splited_rn).count() != 2 \
                    or request.user.id not in splited_rn:
                return HttpResponseRedirect(redirect_url)
            return view_func(request, room_name, *args, **kwargs)
        return _wrapped_view
    return decorator
