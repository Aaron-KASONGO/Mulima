
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('friends', views.friends, name='friends'),
    path('add_friends/<int:id>', views.add_friends, name='add_friends'),
    path('remove_friends/<int:id>', views.remove_friends, name='remove_friends'),
    path('validate_username', views.validate_username, name='validate_username'),
]
