from .client import Redis, StrictRedis
from .connection import (
    ConnectionPool,
    Connection,
    UnixDomainSocketConnection
    )
from .exceptions import (
    AuthenticationError,
    ConnectionError,
    DataError,
    InvalidResponse,
    PubSubError,
    RedisError,
    ResponseError,
    WatchError,
    )


__version__ = '2.4.9'
VERSION = tuple(map(int, __version__.split('.')))

__all__ = [
    'Redis', 'StrictRedis', 'ConnectionPool',
    'Connection', 'UnixDomainSocketConnection',
    'RedisError', 'ConnectionError', 'ResponseError', 'AuthenticationError',
    'InvalidResponse', 'DataError', 'PubSubError', 'WatchError',
    ]
