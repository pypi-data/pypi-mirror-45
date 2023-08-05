import logging
import os

from socketIO_client import SocketIO
from threading import Thread

from .arguments import parse_arguments
from .config import load_config, get_default_config_file
from .exception import SockletArgumentException
from .logging import setup_logger
from .namespace import Namespace
from .server import setup_server

logger = logging.getLogger("socklet")


def bridge_socket(host, port):
    msg = 'Connecting client to {}:{}.'.format(host, port)
    logger.info(msg)

    with SocketIO(host, port, Namespace) as socket:
        socket.wait()


def main():
    setup_logger(logger)

    try:
        args = parse_arguments()
    except SockletArgumentException as e:
        msg = 'Failed to parse arguments: ' + str(e)
        logger.error(msg)
        exit(1)

    if args.debug:
        logger.setLevel(logging.DEBUG)
        msg = "Application is running in debug mode."
        logger.debug(msg)
    elif args.quiet:
        logger.setLevel(logging.WARNING)

    config_file = args.config_file

    if config_file is None:
        config_file = get_default_config_file()

    config = load_config(config_file)

    logger.info("Starting Socklet.")

    def load_parameter(required, conf_section, conf_name, arg_name):
        arg = getattr(args, arg_name, None)

        if arg is not None:
            return arg

        conf = config.get(conf_section, conf_name, fallback=None)

        if not required:
            return conf
        else:
            msg = "Required argument not provided: '{}'."
            logger.error(msg.format(arg_name))
            exit(1)

    client_host = load_parameter(True, 'CLIENT', 'Host', 'client_host')
    client_port = load_parameter(True, 'CLIENT', 'Port', 'client_port')
    server_host = load_parameter(True, 'SERVER', 'Host', 'server_host')
    server_port = load_parameter(True, 'SERVER', 'Port', 'server_port')

    server = setup_server(host=server_host, port=server_port)
    thread_2 = server.consumer
    thread_3 = server.producer

    args = (client_host, client_port)
    thread_1 = Thread(target=bridge_socket, args=args)
    thread_1.start()

    threads = frozenset({thread_1, thread_2, thread_3})

    try:
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        # TODO: Shutdown all threads gracefully.
        os._exit(0)
