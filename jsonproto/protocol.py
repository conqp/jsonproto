"""JSON protocol packets."""

from __future__ import annotations
from json import dumps, loads
from logging import getLogger
from typing import IO, Iterator, NamedTuple

from jsonproto.typing import JSON


__all__ = [
    'MSG_DESPAWN',
    'MSG_SERVER_ERROR',
    'Header',
    'Packet',
    'message',
    'read',
    'write'
]


LOGGER = getLogger('JSON protocol')
MSG_DESPAWN = 'DESPAWN'
MSG_SERVER_ERROR = 'SERVER_ERROR'


class Header(NamedTuple):
    """Header information."""

    followup: bool = False
    big_endian: bool = False
    reserved0: bool = False
    reserved1: bool = False
    reserved2: bool = False
    reserved3: bool = False
    reserved4: bool = False
    reserved5: bool = False

    def __int__(self) -> int:
        """Returns the header as integer."""
        return sum(flag << index for index, flag in enumerate(self))

    def __bytes__(self) -> bytes:
        """Returns the header's bytes."""
        return int(self).to_bytes(1, 'little', signed=False)

    @classmethod
    def from_int(cls, integer: int) -> Header:
        """Creates the header from an int."""
        flags = []

        for bit in range(8):
            flags.append(bool(integer & (1 << bit)))

        return cls(*flags)

    @classmethod
    def from_byte(cls, byte: bytes) -> Header:
        """Creates the protocol header from a byte."""
        return cls.from_int(*list(byte))

    @classmethod
    def read(cls, file: IO) -> Header:
        """Reads the header from a file-like object."""
        return cls.from_byte(file.read(1))

    def write(self, file: IO) -> None:
        """Writes the header to a file-like object."""
        file.write(bytes(self))


class Packet(NamedTuple):
    """A JSON packet."""

    header: Header
    payload: bytes

    @classmethod
    def read(cls, file: IO) -> Packet:
        """Reads a packet from a file-like object."""
        header = Header.read(file)
        size = file.read(4)

        if header.big_endian:
            size = int.from_bytes(size, 'big', signed=False)
        else:
            size = int.from_bytes(size, 'little', signed=False)

        payload = file.read(size)
        return cls(header, payload)

    @property
    def size(self) -> int:
        """Returns the payload size."""
        return len(self.payload)

    def write(self, file: IO) -> None:
        """Writes the packet to a file-like object."""
        self.header.write(file)

        if self.header.big_endian:
            size = self.size.to_bytes(4, 'big', signed=False)
        else:
            size = self.size.to_bytes(4, 'little', signed=False)

        file.write(size)
        file.write(self.payload)


def message(json: JSON) -> JSON:
    """Creates a protocol message from a JSON payload."""

    return {'jsonproto': 'MESSAGE', 'payload': json}


def read(file: IO) -> JSON:
    """Reads a message from a file-like object."""

    packets = []

    while True:
        packets.append(packet := Packet.read(file))
        LOGGER.debug('Read packet: %s', packet)

        if not packet.header.followup:
            break

    return loads(b''.join(packet.payload for packet in packets))


def split_chunks(payload: bytes, chunk_size: int) -> Iterator[bytes]:
    """Splits the payload into chunks."""

    for index in range(0, len(payload), chunk_size):
        yield payload[index:index+chunk_size]


def write(json: JSON, file: IO, *, chunk_size: int = 4096,
          big_endian: bool = False) -> None:
    """Writes a JSON object into a file-like object."""

    payload = dumps(json).encode()
    chunks = list(split_chunks(payload, chunk_size))
    count = len(chunks)

    for index, chunk in enumerate(chunks):
        header = Header(index < count - 1, big_endian)
        packet = Packet(header, chunk)
        packet.write(file)
        LOGGER.debug('Sent packet: %s', packet)
