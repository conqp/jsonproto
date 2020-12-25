"""Common type definitions."""

from ipaddress import IPv4Address, IPv6Address
from typing import Callable, Union


__all__ = ['Handler', 'IPOrHostname', 'JSON']


IPOrHostname = Union[IPv4Address, IPv6Address, str]
JSON = Union[dict, list, str, float, int, bool, None]
Handler = Callable[[JSON], JSON]
