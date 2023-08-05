# -*- coding: utf-8 -*-
"""
Handler Module
--------------

Contains the peer handler and should have nothing else.
"""

__all__ = [
    'PeerHandler',
]

# std imports
import json
import traceback

# package imports
import net

# python 2/3 imports
from net.imports import socketserver


class PeerHandler(socketserver.BaseRequestHandler):
    """
    Handles all incoming requests to the applications Peer server.
    Do not modify or interact with directly.
    """

    # noinspection PyPep8Naming
    def handle(self):
        """
        Handles all incoming requests to the server.
        """
        raw = self.request.recv(1024)

        local_peer = net.Peer()

        # response codes
        null = local_peer.get_flag('NULL').encode('ascii')
        invalid_connection = local_peer.get_flag('INVALID_CONNECTION').encode('ascii')

        # if there is no data, bail and don't respond
        if not raw:
            self.request.sendall(null)
            return

        # convert from json
        try:
            data = raw.decode('ascii')

            try:
                data = json.loads(data)
            except Exception as err:
                net.LOGGER.info("Could not decode server request data: {0}".format(err))

            # skip if there is no data in the request
            if not data:
                self.request.sendall(null)
                return

            # Get the registered connection
            connection = local_peer.registered_connections.get(data['connection'])

            # throw invalid if the connection doesn't exist on this peer.
            if not connection:
                self.request.sendall(invalid_connection)
                return

            # execute the connection handler and send back
            response = connection(*data['args'], **data['kwargs'])

            self.request.sendall(json.dumps(response).encode('ascii'))

        except Exception as err:
            net.LOGGER.error(err)
            net.LOGGER.error(traceback.format_exc())

            packet = {
                'payload': 'error',
                'traceback': traceback.format_exc()
            }

            self.request.sendall(json.dumps(packet).encode('ascii'))
