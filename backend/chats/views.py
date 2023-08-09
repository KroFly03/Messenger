from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from chats.models import Chat, Message
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
        return Chat.objects.get(id=chat_id, participants__in=[self.request.user.id]).messages.all()

    def perform_create(self, serializer):
        chat_id = self.kwargs.get('pk', None)
        serializer.save(chat=chat_id)
