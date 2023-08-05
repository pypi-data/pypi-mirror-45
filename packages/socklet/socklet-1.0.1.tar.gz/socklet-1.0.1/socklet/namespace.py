import logging

from socketIO_client import BaseNamespace

from .server import setup_server
from .event import Event

logger = logging.getLogger("socklet")


class Namespace(BaseNamespace):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.server = setup_server()

        msg = 'Initialized namespace.'
        logger.debug(msg)

    def on_connect(self):
        msg = 'Connection established.'
        logger.info(msg)

    def on_reconnect(self):
        msg = 'Connection reestablished.'
        logger.info(msg)

    def on_disconnect(self):
        msg = 'Connection dissolved.'
        logger.info(msg)

    def on_event(self, event_name, *args):
        msg = "Received event '{}'.".format(event_name)
        logger.debug(msg)

        data = args[0]
        item = Event(event_name, data)
        self.server.send(item)
