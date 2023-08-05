
.. currentmodule:: net

API Reference
=============

Environment
+++++++++++

All of the following are environment variables that can be set to configure net.
Each variable is prefixed with "NET_{value}".

Network Thread Limit
--------------------

.. py:data:: net.THREAD_LIMIT

Default: 5

For larger networks, you may want to increase the thread count. By default, this
is set to 5. When scanning the network for peers, the total number of hosts is
load balanced between the thread count you provide in this variable.

Port Configuration
------------------

.. py:data:: net.PORT_START

Default: 3010

This is the starting port that the peers will attempt to bind to.

.. py:data:: net.PORT_RANGE

Default: 5

This is the range of ports that you want the port to try to bind to. If the
default is 3010, net will scan 3010 - 3015 for a port.

Peer Configuration
------------------

.. py:data:: net.GROUP

Default: None

You can group your peers together by defining the group it belongs to. This
helps Peers find compatible peers or collections.


.. py:data:: net.IS_HUB

Default: False

If you have a single peer that should be the center of an application, you can
identify it through this variable. When you run ``net.info`` on a peer with this
flag, it will return True in the hub field of the friendly_id.

Development Configuration
-------------------------

.. py:data:: net.DEV

Default: None

This will activate the DEBUG level for the net logger. This helps a ton if you
are having trouble tracking communication between peers.


Decorators
++++++++++

.. autofunction:: connect

.. autofunction:: subscribe

.. autofunction:: event

.. autofunction:: flag

Functions
+++++++++

These functions are in place to help with discovering the network and
interacting with other peers.

.. autofunction:: peers

Defaults
++++++++

These are prebuilt flags and handlers for helping get information about peers
and the data flow between peers.

.. autofunction:: info

.. autofunction:: pass_through

Peer
++++

Each instance of python will be assigned a Peer singleton. This is not a true
singleton for development and testing purposes. Although, for production, always
access the peer using the ``net.Peer()`` call. The first thing to understand is
that ``net.Peer()`` is referring to the Peer running in the current instance of
python. So, if you are writing a connection and inside that connection you call
``net.Peer()``. Depending on if that function is being run locally or remotely
will determine which peer you are being returned.

.. autofunction:: Peer

.. autoclass:: net.peer._Peer
    :members: host, id, port, hub, friendly_id, decode_id, generate_id, get_flag, encode, decode

    .. autoattribute:: net.peer._Peer.CONNECTIONS
    .. autoattribute:: net.peer._Peer.SUBSCRIPTIONS
    .. autoattribute:: net.peer._Peer.FLAGS

Full Package
++++++++++++

.. toctree::
   :maxdepth: 7

   modules