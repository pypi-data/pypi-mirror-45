Subscription
============

The files required for this example are:

 * app.py
 * hub.py
 * peer1.py
 * peer2.py

You will need to launch the ``hub.py`` before you launch the peers. After you
launch the hub and however many peers you want, enter in your message and it
will be echoed on all of the peers. A big thing to note is that the peers will
not connect if the hub isn't up. This is because subscriptions only happen when
the peer is launched and there are no re-tries. So any peer launched before the
hub will not get the event triggers.

Feel free to shut down the peers and try to enter your message again. You will
see the hub will not error. It will simply ignore the missing peers. This will
happen if the peers were to fail and error as well. The hub will ignore and just
continue on with its own execution.

app.py
+++++++++

.. literalinclude:: ../../examples/simple_subscription/app.py


hub.py
+++++++++

.. literalinclude:: ../../examples/simple_subscription/hub.py


peer1.py
++++++++

.. literalinclude:: ../../examples/simple_subscription/peer1.py
