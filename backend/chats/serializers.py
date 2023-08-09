from rest_framework import serializers

from chats.models import Message, Chat


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ('created', 'user', 'chat')

    def create(self, validated_data):
        chat = Chat.objects.get(id=validated_data.pop('chat', None))

        message = super().create(validated_data)

        chat.messages.add(message)

        chat.save()

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
