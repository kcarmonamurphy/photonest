from channels.routing import route
from app.websockets import ws_add, ws_message, ws_disconnect

from django.conf import settings

import re

channel_routing = [
    route("websocket.connect", ws_add, path=r'^/' + re.escape(settings.GALLERY_PREFIX) + '/(?P<relative_path>.*)$'),

    route("websocket.receive", ws_message, path=r'^/' + re.escape(settings.GALLERY_PREFIX) + '/(?P<relative_path>.*)$'),

    route("websocket.disconnect", ws_disconnect),
]
