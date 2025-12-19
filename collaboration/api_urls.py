from django.urls import path
from . import views

urlpatterns = [
    path('channels/create/',views.create_channel),
    path('channels/',views.list_channels),
    path('messages/send/',views.send_message),
    path('messages/',views.list_messages),
    path('debug-auth/', views.debug_auth),
]