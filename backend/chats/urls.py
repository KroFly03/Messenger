from django.urls import path

from chats.views import ChatView, MessageView

urlpatterns = [
    path('chats/', ChatView.as_view()),
    path('chats/<int:pk>/messages/', MessageView.as_view())
]
