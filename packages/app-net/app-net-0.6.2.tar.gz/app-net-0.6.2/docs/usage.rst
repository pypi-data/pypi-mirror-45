=====
Usage
=====

Core Concepts
-------------
app-net uses peer-to-peer socket servers to execute code both locally and remotely. The first
thing to understand is the difference between **local** and **remote** execution of a function.

Local
+++++
When you launch python and you execute a function, it will execute inside that instance, obviously.
app-net requires you the developer to define the peer id to execute the function on. If you don't
tell the function where to execute the code, it will default to a normal pass-through. This makes
development and testing easier. The response locally is expected to match a remote peers response.

Remote
++++++
When you execute a function, you can tell it to **connect** to a different instance of python,
execute the code, and return the result through the socket response. The thing to understand is
that a **remote** instance doesn't need to be on another host. Meaning, if you have 2 instances
of python running app-net on the same host, they can communicate the same way they would if they
were on a different host.

A Basic Example
---------------

This is a very simple example of an application running on 2 different peers and communicating
through a shared coding contract, the application itself.

app.py
++++++

.. literalinclude:: ../examples/simple_connection/app.py


peer1.py
++++++++

.. literalinclude:: ../examples/simple_connection/peer1.py

peer2.py
++++++++

.. literalinclude:: ../examples/simple_connection/peer2.py