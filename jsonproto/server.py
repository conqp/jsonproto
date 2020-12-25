"""A JSON protocol server."""

from logging import getLogger
from socket import socket
from traceback import format_exc

from jsonproto.exceptions import Despawn
from jsonproto.protocol import MSG_DESPAWN
from jsonproto.protocol import MSG_SERVER_ERROR
from jsonproto.protocol import message
from jsonproto.protocol import read
from jsonproto.protocol import write
from jsonproto.typing import IPOrHostname, Handler


__all__ = ['spawn']


LOGGER = getLogger('JSON Server')


def spawn(host: IPOrHostname, port: int, handler: Handler, *,
          chunk_size: int = 4096, big_endian: bool = False) -> None:
    """Spawns a server."""

    with socket() as sock:
        sock.bind((str(host), port))
        sock.listen()

        while True:
            try:
                conn, address = sock.accept()
            except KeyboardInterrupt:
                LOGGER.info('User abort.')
                break

            LOGGER.info('Incoming connection from %s.', address)

            with conn.makefile('rb') as file:
                json = read(file)

            try:
                json = handler(json['payload'])
            except Despawn:
                json = {'jsonproto': MSG_DESPAWN}
            except Exception as error:  # pylint: disable=W0703
                LOGGER.fatal('Caught unhandled exception: %s', error)
                json = {
                    'jsonproto': MSG_SERVER_ERROR,
                    'exception': str(error),
                    'type': str(type(error)),
                    'stacktrace': format_exc()
                }
            else:
                json = message(json)

            with conn.makefile('wb') as file:
                write(json, file, chunk_size=chunk_size, big_endian=big_endian)

            if json.get('jsonproto') in {MSG_DESPAWN, MSG_SERVER_ERROR}:
                LOGGER.info('Despawning.')
                break
