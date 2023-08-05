import asyncio
import logging

from queue import Queue
from threading import Thread, Lock
from websockets import serve
from websockets.exceptions import ConnectionClosed

from .decorators import static_variable

logger = logging.getLogger("socklet")


@static_variable(server=None)
def setup_server(host=None, port=None):
    if setup_server.server is None:
        if host is None or port is None:
            msg = 'Cannot setup server without host and port.'
            raise Exception(msg)
        else:
            setup_server.server = Server(host, port)

    return setup_server.server


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        msg = 'Setup server listening on {}:{}.'.format(self.host, self.port)
        logger.info(msg)

        self.queue = Queue()
        self.clients = set()
        self.lock = Lock()

        self.consumer = Thread(target=self.run_consumer)
        self.consumer.start()

        self.producer = Thread(target=self.run_producer)
        self.producer.start()

    def run_consumer(self):
        msg = 'Setting up consumer.'
        logger.debug(msg)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def consumer_handler(websocket, path):
            msg = 'Client {} connected.'.format(id(websocket))
            logger.info(msg)

            try:
                self.lock.acquire()
                self.clients.add(websocket)
            finally:
                self.lock.release()

            try:
                async for message in websocket:  # noqa: F841
                    pass
            except ConnectionClosed:
                pass
            finally:
                try:
                    self.lock.acquire()
                    self.clients.remove(websocket)

                    msg = 'Client {} disconnected.'.format(id(websocket))
                    logger.info(msg)
                finally:
                    self.lock.release()

        start_server = serve(consumer_handler, self.host, self.port)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    def run_producer(self):
        msg = 'Setting up producer.'
        logger.debug(msg)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def send(client, message):
            try:
                await client.send(message)
            except ConnectionClosed:
                pass

        async def broadcast(item):
            msg = 'Sending message {} to clients.'.format(id(item))
            logger.debug(msg)

            message = str(item)

            if len(self.clients) > 0:
                await asyncio.wait([send(c, message) for c in self.clients])

        while True:
            msg = 'Waiting for next item in sending queue.'
            logger.debug(msg)

            item = self.queue.get()

            try:
                self.lock.acquire()

                loop = asyncio.get_event_loop()
                coro = broadcast(item)
                loop.run_until_complete(coro)
            finally:
                self.lock.release()

    def send(self, item):
        msg = 'Putting item in sending queue.'
        logger.debug(msg)

        self.queue.put(item)
