from chats.models import Chat, Message


def send(message_id, chat_id):

    chat = Chat.objects.get(id=chat_id)

    message = Message.objects.get(id=message_id)

    chat.messages.add(message)

    chat.save()


def receive(message_id):
    message = Message.objects.get(id=message_id)

    message.status = Message.Status.RECEIVED

    message.save()
