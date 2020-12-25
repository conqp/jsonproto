"""Client implementation for the JSON protocol."""

from socket import socket
from typing import Optional

from jsonproto.protocol import message, read, write
from jsonproto.typing import IPOrHostname, JSON


__all__ = ['Client']


class Client:
    """A basic client for the JSON protocol."""

    def __init__(self, host: IPOrHostname, port: int, *,
                 timeout: Optional[int] = None):
        """Sets the target server's address or host name and port."""
        self.host = host
        self.port = port
        self.timeout = timeout
        self._socket = socket()

    def __enter__(self):
        self._socket.__enter__()
        self._socket.settimeout(self.timeout)
        self._socket.connect((str(self.host), self.port))
        return self

    def __exit__(self, typ, value, traceback):
        return self._socket.__exit__(typ, value, traceback)

    def communicate(self, json: JSON, *, chunk_size: int = 4096,
                    big_endian: bool = False) -> JSON:
        """Sends and receives a message."""
        with self._socket.makefile('wb') as file:
            write(message(json), file, chunk_size=chunk_size,
                  big_endian=big_endian)

        with self._socket.makefile('rb') as file:
            return read(file)['payload']
