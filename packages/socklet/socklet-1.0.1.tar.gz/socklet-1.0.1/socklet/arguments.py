import logging

from argparse import ArgumentParser

from .exception import SockletArgumentException

logger = logging.getLogger("socklet")


def parse_arguments():
    parser = ArgumentParser(
        prog="socklet",
        description="A tool for bridging Socket.IO 0.9 to WebSocket."
    )
    parser.add_argument("-v", "--debug", action="store_true",
                        help="Print debug information.")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Print errors and warnings only.")
    parser.add_argument("-c", "--config-file", type=str,
                        help="File to read configuration from.")
    parser.add_argument("--client-host", type=str,
                        help="Hostname to connect to.")
    parser.add_argument("--client-port", type=int,
                        help="Port to connect to.")
    parser.add_argument("--server-host", type=str,
                        help="Hostname to listen on.")
    parser.add_argument("--server-port", type=int,
                        help="Port to listen on.")

    args = parser.parse_args()

    if args.debug and args.quiet:
        msg = 'Cannot be quiet in debug mode.'
        raise SockletArgumentException(msg)

    return args
