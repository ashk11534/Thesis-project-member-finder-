from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('create-room/<int:user_id>/<str:page_name>', views.create_room, name='create-room'),
    path('room/<int:room_id>', views.room, name='room'),
    path('join-room/<int:room_id>/<int:user_id>', views.join_room, name='join-room'),
    path('send-message', views.send_message, name='send-message'),
    path('delete-message/<int:message_id>/<int:room_id>', views.delete_message, name='delete-message'),
    path('delete-user-message/<int:message_id>/<int:user_id>', views.delete_user_message, name='delete-user-message'),
    path('delete-all-user-message/<int:user_id>', views.delete_all_user_message, name='delete-all-user-message'),
    path('user-message/<int:sender_id>/<int:receiver_id>', views.user_message, name='user-message'),
    path('received-messages/<int:user_id>', views.received_messages, name='received-messages'),
    path('update-room/<int:room_id>', views.update_room, name='update-room'),
    path('user-profile/<int:user_id>', views.user_profile, name="user-profile"),
    path('update-profile/<str:page_name>', views.update_profile, name='update-profile'),
    path('user-signup', views.user_signup, name='signup'),
    path('user-login', views.login_user, name='login'),
    path('user-logout', views.user_logout, name='logout'),
    path('delete-room/<int:id>/<int:user_id>/<str:page_name>', views.delete_room, name='delete-room')
]
