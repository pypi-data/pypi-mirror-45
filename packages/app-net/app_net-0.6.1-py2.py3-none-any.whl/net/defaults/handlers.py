# -*- coding: utf-8 -*-
"""
Default Connected Handlers
--------------------------

Prebuilt connected handlers for net. Do not modify.
"""
# python imports
import sys
import getpass

# package imports
import net

__all__ = [
    'info',
    'pass_through',
    'null',
    'subscription_handler',
    'connections'
]


# basic descriptor
@net.connect()
def info(*args, **kwargs):
    """
    Return information about the peer requested.

    .. code-block:: python

        friendly_information = net.info(peer='somepeer')

    :return: peer.friendly_id
    """
    information = net.Peer()
    return {
        # friendly tag
        'tag': str(information),

        # host
        'host': information.host,
        'port': information.port,

        # user
        'user': getpass.getuser(),
        'executable': sys.executable,

        # app
        'group': information.group,
        'hub': information.hub,

        # interfaces
        'connections': sorted(list(information.registered_connections.keys())),
        'subscriptions': sorted(list(information.registered_subscriptions.keys())),
        'flags': sorted(list(information.registered_flags.keys())),
    }


# basic connection descriptor
@net.connect()
def connections(*args, **kwargs):
    """
    Return the connections registered with the peer.

    .. code-block:: python

        friendly_information = net.connections(peer='somepeer')

    :return: peer.CONNECTIONS
    """
    registered_connections = net.Peer().registered_connections

    return 'Connections on {1}:\n\t{0}'.format(
        '\n\n\t'.join(
            [
                '{0}\n\t\t{1}'.format(
                    key,
                    registered_connections[key]) for key in registered_connections.keys()
            ]
        ),
        net.Peer().friendly_id
    )


# utilities
@net.connect()
def pass_through(*args, **kwargs):
    """
    Used for testing, takes your arguments and passes them back for type
    testing.

    .. code-block:: python

        variable = "Test this comes back the way I sent it."

        response = net.pass_through(variable, peer='somepeer')

    :return: *args, **kwargs
    """
    if len(args) == 1:
        return args[0]
    return args, kwargs


@net.connect()
def null(*args, **kwargs):
    """
    Return a null response flag

    :return: NULL Flag
    """
    return net.Peer().get_flag("NULL")


@net.connect()
def subscription_handler(event, host, port, connection, *args, **kwargs):
    """
    Will register the incoming peer and connection with the local peers
    subscription of the event passed. This is for internal use only.

    :param event: event id
    :param host: foreign peer host
    :param port: foreign peer port
    :param connection: connection id
    """
    net.Peer().register_subscriber(event, host, port, connection)
