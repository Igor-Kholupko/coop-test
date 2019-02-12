from django.urls import path

from chat import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<room_name>/', views.room, name='room'),
    path('home/<user_id>/', views.home, name='home'),
]
