# -*- coding: utf-8 -*-
"""
Peer Server Module
------------------

Contains the server engine for the peer.
"""

__all__ = ['PeerServer']

# std imports
import re
import json
import socket
import traceback
import threading

# compatibility
from six import add_metaclass

# package imports
import net

# package imports
from net.peer.handler import PeerHandler
from net.imports import socketserver, ConnectionRefusedError


# globals
SINGLETON = None

# utilities
ID_REGEX = re.compile(r"(?P<host>.+):(?P<port>\d+) -> (?P<group>.+)")

# threading
LOCK = threading.Lock()


class SingletonServer(type):
    """
    This protects the server from being replicated unless it is for testing.
    """
    instance = None

    def __call__(cls, *args, **kwargs):

        if kwargs.get('test'):
            return super(SingletonServer, cls).__call__(*args, **kwargs)

        if not cls.instance:
            cls.instance = super(SingletonServer, cls).__call__(*args, **kwargs)

        return cls.instance


# noinspection PyMissingConstructor
@add_metaclass(SingletonServer)
class PeerServer(socketserver.ThreadingMixIn, socketserver.TCPServer, object):
    # adding to inheritance object for 2.7 support
    """
    Base PeerServer class that handles all incoming and outgoing requests.
    """

    @staticmethod
    def ports():
        """
        Generator; All ports defined in the environment.

        :return: int
        """
        return [port for port in range(net.PORT_START, net.PORT_START + net.PORT_RANGE)]

    @staticmethod
    def ping(port, host=socket.gethostname()):
        """
        Ping a port and check if it is alive or open.

        :param port: required port to hit
        :param host: host address default is 'localhost'
        :return: bool
        """

        # sockets
        interface = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        interface.settimeout(0.25)
        try:
            interface.connect((host, port))
            interface.close()
            return True
        except (ConnectionRefusedError, socket.error):
            return False

    def __init__(self, test=False):

        # descriptor
        self._host = net.HOST_IP
        self._port = self.scan_for_port()

        # handle threading
        self._thread = threading.Thread(target=self.serve_forever)
        self._thread.daemon = True

        # launch the server
        self._thread.start()

    @property
    def port(self):
        """
        Port that the peer is running on.

        :return: int
        """
        return self._port

    @property
    def host(self):
        """
        Host that the peer is running on.

        :return: str
        """
        return self._host

    def scan_for_port(self):
        """
        Scan for a free port to bind to. You can override the default port range
        and search range by setting the environment variables NET_PORT
        NET_PORT_RANGE.

        Port range:
            default 3010-3050

        :return: int
        """
        # cast as int and default to 3010 and 40
        port = net.PORT_START
        port_range = port + net.PORT_RANGE

        net.LOGGER.debug("Scanning {0} ports for open port...".format(port_range - port))
        while port <= port_range:

            # ping the local host ports
            if not self.ping(port):
                try:
                    super(PeerServer, self).__init__((self.host, port), PeerHandler)
                    net.LOGGER.debug("Stale Port: {0}".format(port))
                except (OSError, socket.error):
                    continue
                net.LOGGER.debug("Found Port: {0}".format(port))
                return port

            port += 1

        # throw error if there is no open port
        if port > port_range:
            raise ValueError("No open port found between {0} - {1}".format(port, port_range))

    @staticmethod
    def request(host, port, connection, args, kwargs):
        """
        Request an action and response from a peer.

        :param host: target host ipv4 format
        :param port: target port int
        :param connection: the target connection id to run
        :param args: positional arguments to pass to the target connection (must be json compatible)
        :param kwargs: keyword arguments to pass to the target connection (must be json compatible)
        :return: response from peer
        """
        # socket connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # set the time out on the function
        if kwargs.get('time_out'):
            sock.settimeout(kwargs.get('time_out'))

        # connect
        sock.connect((host, port))

        # convert the data to json and then bytes
        data = {'connection': connection, 'args': args, 'kwargs': kwargs}

        try:
            data = json.dumps(data)
        except TypeError:
            data = str(data)

        payload = data.encode('ascii')

        try:
            # send request
            sock.sendall(payload)

            # sock
            raw = sock.recv(1024)

            # safely close the socket
            sock.close()

        except Exception as err:
            # safely close the socket
            sock.close()

            # handle error logging
            net.LOGGER.error(traceback.format_exc())
            raise err

        response = raw.decode('ascii')
        try:
            return json.loads(response)
        except Exception:
            return response

    def protected_request(self, host, port, connection, args, kwargs, stale):
        """
        This allows for protected requests. Intended for threaded event calls.

        .. warning::

            INTERNAL USE ONLY
            Do not use this directly, it will only cause you pain.

        :param host: target host ipv4 format
        :param port: target port int
        :param connection: the target connection id to run
        :param args: positional arguments to pass to the target connection (must be json compatible)
        :param kwargs: keyword arguments to pass to the target connection (must be json compatible)
        :param stale: share resource for detecting old peers
        :return: response from peer
        """
        try:
            self.request(host, port, connection, args, kwargs)
        except Exception as e:
            if isinstance(e, ConnectionRefusedError):

                # thread handling
                LOCK.acquire()
                stale.append((host, port))
                LOCK.release()

            else:
                net.LOGGER.warning(
                    "An error has happened a remote peer. "
                    "This was a protected request and will "
                    "ignore the error response.\n\t"
                    "Peer: {0}".format((host, port))
                )
