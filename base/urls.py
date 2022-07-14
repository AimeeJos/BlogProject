from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('room/<str:pk>/',views.room,name="room"),
    path('create-room/',views.createRoom,name='create-room'),
    path('update-room/<str:pk>',views.updateRoom,name='update-room'),
    path('delete-room/<str:pk>', views.deleteRoom, name='delete-room'),
    path('login', views.userlogin, name='login'),
    path('logout', views.userlogout, name='logout'),
    path('register', views.registeruser, name='register'),
    path('delete-msg/<str:pk>', views.deleteMsg, name='delete-msg'),
    path('profile/<str:pk>', views.userProfile, name='profile'),

]