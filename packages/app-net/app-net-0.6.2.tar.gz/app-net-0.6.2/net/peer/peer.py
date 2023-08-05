# -*- coding: utf-8 -*-
"""
Peer Object Module
------------------

Contains the Peer object descriptor.
"""

__all__ = ['Peer']

# std imports
import re
import copy
import functools
import threading

# compatibility
from six import add_metaclass

# package imports
import net

# utilities
ID_REGEX = re.compile(r"(?P<host>.+):(?P<port>\d+) -> (?P<group>.+)")

# threading
LOCK = threading.Lock()


class SingletonPeer(type):
    """
    This allows for the dev to request a peer
    """
    instance = None

    def __call__(cls, *args, **kwargs):
        if kwargs.get('host') and kwargs.get('port') or kwargs.get('test'):
            return super(SingletonPeer, cls).__call__(*args, **kwargs)

        if not cls.instance:
            cls.instance = super(SingletonPeer, cls).__call__(*args, **kwargs)

        return cls.instance


@add_metaclass(SingletonPeer)
class Peer(object):
    # adding to inheritance object for 2.7 support
    """
    Base Peer class that defines interactions between peers.
    """

    @staticmethod
    def build_connection_name(connection):
        """
        Build a connections full name based on the module/name of the function.

        :param connection: connection
        :return: connection path
        """
        return '.'.join([connection.__module__, connection.__name__])

    def __repr__(self):
        return '<net.Peer h:{0} p:{1} g:{2} c:{3} s:{4} f:{5}>'.format(
            str(self.host),
            str(self.port),
            str(self.group),
            len(self.registered_connections),
            len(self.registered_subscriptions),
            len(self.registered_flags),
        )

    def __init__(
            self,
            host=None,
            port=None,
            group=None,
            hub=False,
            subscriptions=None,
            connections=None,
            flags=None,
            test=False
    ):

        # describing factors about this peer.
        self._group = group if group else net.GROUP
        self._port = port
        self._host = host
        self._is_hub = hub if hub else net.IS_HUB
        self._server = net.PeerServer(test=test)

        # instance connections
        self._registered_subscriptions = subscriptions if subscriptions else {}
        self._registered_connections = connections if connections else {}
        self._registered_flags = flags if flags else {}
        self._tag_map = {}

        # load information about the remote peer.
        if self.host and self.port:
            self.load_remote_connections()

    @property
    def server(self):
        """
        Reference to the server engine.

        :return: bool
        """
        return self._server

    @property
    def hub(self):
        """
        Defines if this peer acts as the hub for communication through the
        network.

        :return: bool
        """
        return self._is_hub

    @property
    def group(self):
        """
        Group this peer is assigned to.

        :return: str
        """
        return self._group

    @property
    def port(self):
        """
        Port that the peer is running on.

        :return: int
        """
        if not self._port:
            return self.server.port
        return self._port

    @property
    def host(self):
        """
        Host that the peer is running on.

        :return: str
        """
        if not self._host:
            return self.server.host
        return self._host

    @property
    def registered_connections(self):
        """
        Get all connections registered with this peer.

        :return:
        """
        return self._registered_connections

    @property
    def registered_subscriptions(self):
        """
        Get all subscriptions registered with this peer.

        :return:
        """
        return self._registered_subscriptions

    @property
    def registered_flags(self):
        """
        Get all flags registered with this peer.

        :return:
        """
        return self._registered_flags

    def mask_as_remote(self, func):
        """
        Used for testing.

        :return:
        """
        @functools.wraps(func)
        def wrap(*args, **kwargs):
            net.LOGGER.debug("REMOTE request {0} (simulated)".format(self))
            return func(peer=(self.host, self.port), *args, **kwargs)

        return wrap

    def load_remote_connections(self):
        """
        Loads the connections from the remote peers information.

        DO NOT USE DIRECTLY

        :return: None
        """

        for connection in self.registered_connections:

            def tag_wrapper(tag, *args, **kwargs):
                net.LOGGER.debug("REMOTE request {0}".format(self))
                return self.execute((self.host, self.port), tag, args, kwargs)

            connection_path = connection.rsplit('.')
            connection_path.reverse()
            tag = connection_path[0]

            setattr(self, tag, functools.partial(tag_wrapper, connection))

    def register_connection(self, connection, tag=None):
        """
        Registers a connection with the global handler.
        Do not use this directly. Instead use the net.connect decorator.

        :param connection: function
        :param tag: str
        :return: str
        """
        # generate the functions tag
        func_tag = self.build_connection_name(connection)

        # add the connection to the connection registry.
        if tag in self.registered_connections or func_tag in self.registered_connections:
            net.LOGGER.warning(
                "Redefining a connection handler. Be aware, this could cause "
                "unexpected results."
            )

        # register both the function tag and the passed tag if there is one passed
        self.registered_connections[func_tag] = connection
        setattr(self, func_tag.rsplit('.', 1)[1], connection)
        if tag:
            self.registered_connections[tag] = connection
            setattr(self, tag, connection)

        return tag if tag else func_tag

    def register_subscriber(self, event, host, port, connection):
        """
        Registers the peer and connection to the peers subscription system. This
        is for internal use only, use the ``net.subscribe`` decorator instead.

        :param event: event id
        :param host: str
        :param port: int
        :param connection: connection id
        :return: None
        """
        subscription = self.registered_subscriptions.setdefault(event, {})
        peer_connection = subscription.setdefault((host, port), [])
        peer_connection.append(connection)

    def register_flag(self, flag, handler):
        """
        Registers a flag with the peer server. Flags are simple responses that
        can trigger error handling or logging. Do not use this directly. Instead
        use the net.flag decorator.

        @net.flag("SOME_ERROR")
        def your_next_function(peer, connection):
            raise SomeError(
                "This failed because {0} failed on the other peer.".format(
                    connection
                )
            )

        :param flag: payload
        :param handler: function
        :return: base64
        """
        if flag in self.registered_flags:
            net.LOGGER.warning(
                "Redefining a flag handler. Be aware, this could cause "
                "unexpected results."
            )

        self.registered_flags[flag] = handler

        return flag

    @staticmethod
    def process_flags(response, connection, peer):
        """
        Check a response and test if it should be processed as a flag.

        :param response: Anything
        :param connection:
        :param peer:
        :return: response from the registered process
        """
        # handle flags
        try:
            if response in Peer().registered_flags:
                return Peer().registered_flags[response](connection, peer)
        except TypeError:
            pass

    def get_flag(self, flag):
        """
        Get a flags id.

        :param flag: str
        :return: str
        """
        # validate the flag requested
        if flag not in self.registered_flags:
            raise Exception("Invalid Flag requested.")

        return flag

    def execute(self, peer, connection, args, kwargs):
        """
        Execute a request on a remote peer. This should not be used directly.
        Use the decorators ``net.connect`` and ``net.event`` to trigger an
        execution on a remote peer.

        :param peer: ``net.Peer`` or (host, port)
        :param connection: the target connection id to run
        :param args: positional arguments to pass to the target connection (must be json compatible)
        :param kwargs: keyword arguments to pass to the target connection (must be json compatible)
        :return:
        """
        if isinstance(peer, tuple):
            host = peer[0]
            port = peer[1]
        else:
            host = peer.host
            port = peer.port

        response = self._server.request(host, port, connection, args, kwargs)

        try:
            if response in self.registered_flags:
                response = self.process_flags(response, connection, peer)
        except TypeError:
            pass

        return response

    def trigger_event(self, event, *args, **kwargs):
        """
        Registers the peer and connection to the peers subscription system. This
        is for internal use only, use the ``net.subscribe`` decorator instead.

        :param event: event id
        :param args: args to pass to the subscribed connections
        :param kwargs: args to pass to the subscribed connections
        :return: None
        """
        event = self.registered_subscriptions.get(event)

        if not event:
            net.LOGGER.info(
                "Invalid Event {0}.\n"
                "This event has no subscribers so it will be skipped."
                "Active Events:\n" + '\n'.join(
                    sorted(self.registered_subscriptions.keys())
                )
            )
            return

        # loop over the peers
        stale = []

        # thread spawning variables
        threads = []

        # loop over and multi thread the requests
        for peer, connections in event.items():
            for connection in connections:
                host, port = peer

                # try to execute the subscription trigger on the subscribed peer
                # For the purpose of protecting the event triggering peer from
                # remote errors, all connection errors and remote runtime errors
                # will be caught and logged. But nothing will halt the running
                # application. i.e. this peer.
                #
                # Stale peer subscriptions will be added to the stale list and
                # pruned. Since the list subscriptions are created per client
                # request, this peer will not know until a request is made that
                # the subscribed peer went offline.
                if net.THREAD_LIMIT == 0:
                    self.server.protected_request(
                        host,
                        port,
                        connection,
                        args,
                        kwargs,
                        stale
                    )
                    continue

                # if multi-threading is configured, distribute the workload to
                # the threads.
                thread = threading.Thread(
                    target=self.server.protected_request,
                    args=(host, port, connection, args, kwargs, stale)
                )
                thread.setName(
                    "Network_Worker_{0}_{1}".format(peer, connection)
                )
                thread.daemon = True
                threads.append(thread)
                thread.start()

                # if we hit the configured thread limit, wait until we free up
                # some threads
                if len(threads) == net.THREAD_LIMIT:
                    for thread in threads:
                        thread.join()

                    # reset the threads list and continue requesting
                    threads = []

        # safety catch in case there are still some working threads
        for thread in threads:
            thread.join()

        # create a working copy before we prune
        updated_subscriptions = copy.deepcopy(self.registered_subscriptions)

        # Clean out the stale peers that are no longer valid.
        for event, event_data in self.registered_subscriptions.items():

            # clean out the offline or unreachable peers
            for stale_address in stale:
                if stale_address in event_data:
                    del updated_subscriptions[event][stale_address]

            # delete the event if it is empty
            if not event_data.keys():
                del updated_subscriptions[event]

        # update the subscriptions registry
        self._registered_subscriptions = updated_subscriptions
