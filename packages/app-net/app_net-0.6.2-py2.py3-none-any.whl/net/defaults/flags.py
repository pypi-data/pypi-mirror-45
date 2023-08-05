# -*- coding: utf-8 -*-
"""
Default Flags
-------------

Prebuilt flags for net. Do not modify.
"""

# std imports
import base64

# package imports
import net

__all__ = [
    'null_response',
    'invalid_connection'
]


# Flags
@net.flag('NULL')
def null_response(connection, peer):
    """
    Execute this if the peer has returned the NULL_RESPONSE flag.

    :param connection: name of the connection requested
    :param peer: ``net.Peer``
    :return: str
    """
    return "NULL"


# Flags
@net.flag('INVALID_CONNECTION')
def invalid_connection(connection, peer):
    """
    Execute this if the peer has returned the NULL_RESPONSE flag.

    :param connection: name of the connection requested
    :param peer: ``net.Peer`` or tuple
    :return:
    """
    if isinstance(peer, tuple):
        host = peer[0]
        port = peer[1]
        connections = [str(connection) for connection in net.Peer().registered_connections.keys()]
    else:
        host = peer.host
        port = peer.port
        connections = peer.registered_connections

    raise Exception(
        "Peer does not have the connection you are requesting.\n\t"
        "Peer: {0}@{1}\n\t"
        "Registered Connections: \n\t\t{3}\n\t"
        "Connection Requested: {2}".format(
            host,
            port,
            connection,
            '\n\t\t'.join(connections)
        )
    )
