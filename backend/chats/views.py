from django.http import Http404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from chats.models import Chat
from chats.serializers import ChatSerializer, MessageSerializer


class ChatView(generics.ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Chat.objects.filter(participants__in=[self.request.user.id])


class MessageView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        chat_id = self.kwargs.get('pk', None)

        try:
            messages = Chat.objects.get(id=chat_id, participants__in=[self.request.user.id]).messages.all()
        except Chat.DoesNotExist:
            raise Http404()

        return messages

    def perform_create(self, serializer):
        chat_id = self.kwargs.get('pk', None)
        serializer.save(chat=chat_id)
