from chats.serivce import send, receive
from messenger.celery import app


@app.task
def send_message(message_id, chat_id):
    send(message_id, chat_id)


@app.task
def receive_message(message_id):
    receive(message_id)
