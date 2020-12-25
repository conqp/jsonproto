"""JSON protocol exceptions."""

__all__ = ['Despawn', 'NoResponse']


class Despawn(Exception):
    """Signals the server to shut down."""


class NoResponse(Exception):
    """Signals the server to not send a response."""
