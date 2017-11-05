from .path import Path
from .scandir import parse_path

# Connected to websocket.connect
def ws_add(message, relative_path):
    # Accept the connection
    message.reply_channel.send({"accept": True})

# Connected to websocket.receive
def ws_message(message, relative_path):

    if (message.content['text'] == 'parse_path'):
        # Scan the directory specified by the path
        # and use websockets to send information
        # back to the browser
        parse_path(Path(relative_path), message)

# Connected to websocket.disconnect
def ws_disconnect(message):
    pass
    # message.discard(message.reply_channel)