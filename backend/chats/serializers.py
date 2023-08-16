from django.db import transaction
from django.http import Http404
from rest_framework import serializers

from chats.models import Message, Chat
from chats.tasks import send_message, receive_message


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ('created', 'user', 'chat')

    def create(self, validated_data):
        with transaction.atomic():
            chat_id = validated_data.pop('chat', None)
            sender = validated_data.get('sender', None)

            try:
                Chat.objects.get(id=chat_id, participants__in=[sender])
            except Chat.DoesNotExist:
                raise Http404()

            message = super().create(validated_data)

            send_message.delay(message.id, chat_id)
            receive_message.apply_async(args=[message.id], countdown=10)

            return message


class ChatSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Chat
        fields = '__all__'
        read_only_fields = ('messages', 'user', 'created')

    def create(self, validated_data):
        participants = validated_data.get('participants', None)
        user = validated_data.pop('user', None)

        if user not in participants:
            participants.append(user)
            validated_data['participants'] = participants

        return super().create(validated_data)
