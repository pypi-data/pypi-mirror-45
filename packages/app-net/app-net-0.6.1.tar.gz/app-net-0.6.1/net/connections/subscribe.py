# -*- coding: utf-8 -*-
"""
Subscribe Module
----------------

Contains the subscribe decorator and should have nothing else.
"""

__all__ = [
    'subscribe'
]

# package imports
import net


def subscribe(event, groups=None, hubs_only=False, peers=None, on_host=None):
    """
    Subscribe to an event on another peer or set of peers. When the peer
    triggers an event using ``net.event``, the peer will take the arguments
    passed and forward them to this function. By default, this will subscribe to
    all peers. You can also manually filter the peers by selectively passing in
    only the peers you want to subscribe to using the ``peers`` keyword argument.

    Subscribe to "some_event" on group1 peers only.

    .. code-block:: python

        group1_peers = net.peers(groups=['group1'])

        @net.subscribe("some_event", group1_peers)
        def your_function(subscription_args, subscription_kwarg=None):
            return some_value

    Subscribe to "some_event" on a single peer.

    .. code-block:: python

        peer = net.peers()[0]

        @net.subscribe("some_event", peer)
        def your_function(subscription_args, subscription_kwarg=None):
            return some_value

    Subscribe to "some_event" on all peers.

    .. code-block:: python

        @net.subscribe("some_event")
        def your_function(subscription_args, subscription_kwarg=None):
            return some_value

    """
    this_peer = net.Peer()

    # handle peers arg
    if not peers:
        peers = net.peers(
            hubs_only=hubs_only,
            groups=groups,
            on_host=on_host
        )['peers'].values()
    else:
        if not isinstance(peers, (list, tuple)):
            peers = [peers]

    def wrapper(func):

        # build the connection id
        connection = this_peer.register_connection(func)

        # loop over all the requested peers
        for peer in peers:
            peer.subscription_handler(event, this_peer.host, this_peer.port, connection)

        return func
    return wrapper
