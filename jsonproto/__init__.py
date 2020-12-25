"""A network protocol for client / server communication via JSON."""

from jsonproto.client import Client
from jsonproto.exceptions import Despawn
from jsonproto.protocol import MSG_DESPAWN
from jsonproto.protocol import MSG_SERVER_ERROR
from jsonproto.protocol import Header
from jsonproto.protocol import Packet
from jsonproto.protocol import message
from jsonproto.protocol import read
from jsonproto.protocol import write
from jsonproto.server import spawn
from jsonproto.typing import Handler
from jsonproto.typing import IPOrHostname
from jsonproto.typing import JSON


__all__ = [
    'MSG_DESPAWN',
    'MSG_SERVER_ERROR',
    'Despawn',
    'Client',
    'Handler',
    'Header',
    'IPOrHostname',
    'JSON',
    'Packet',
    'message',
    'read',
    'spawn',
    'write'
]
