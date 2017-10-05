import os
from channels.asgi import get_channel_layer


"""
ASGI entrypoint file for default channel layer.
Points to the channel layer configured as "default" so you can point
ASGI applications at "multichat.asgi:channel_layer" as their channel layer.
"""
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "notgoogleplus.settings.development")
channel_layer = get_channel_layer()
