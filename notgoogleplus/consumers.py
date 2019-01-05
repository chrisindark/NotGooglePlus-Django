# consumers.py
def websocket_receive(message):
    print('websocket message')
    text = message.content.get('text')
    if text:
        message.reply_channel.send({"text": "You said: {}".format(text)})
