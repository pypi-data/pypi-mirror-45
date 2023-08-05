#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

"""Tests for `net` package."""

# std imports
import functools
import traceback

# testing
import pytest

# package
import net


@pytest.fixture(scope="module")
def peers():
    """
    Set up the peers for testing.
    """
    net.LOGGER.debug("Test Header")

    master = net.Peer()
    slave = net.Peer(test=True)

    @net.connect()
    def force_error(*args, **kwargs):
        raise Exception

    # need to register the default functions for testing
    slave.register_connection(slave.mask_as_remote(net.pass_through))
    slave.register_connection(slave.mask_as_remote(net.null))
    slave.register_connection(slave.mask_as_remote(force_error))
    slave.register_connection(slave.mask_as_remote(net.subscription_handler))

    yield master, slave


def test_peer_construct(peers):
    """
    Construct and connect 2 peer servers.
    """
    net.LOGGER.debug("Test Header")

    master, slave = peers

    assert master.port != slave.port
    assert not master.hub
    assert slave.server.ping(master.port, master.host) is True
    assert master.server.ping(slave.port, slave.host) is True


def test_connect_decorator(peers):
    """
    Test the connect decorator
    """
    net.LOGGER.debug("Test Header")

    master, slave = peers

    test_cases = [
        # dict types
        {"testing": "value"}, {"1": 1}, {"1": {"2": 3}},

        # array types. Tuples aren't supported at the moment
        [1, "1", 1.0],

        # strings types
        "This is a string", "",

        # None type
        None,

        # bool types
        True, False,

        # number types
        1.0, 1,
    ]

    # loop over each test case and make sure a remote response equals to a local response.
    for case in test_cases:
        master_response = master.pass_through(case)
        slave_response = slave.pass_through(case)
        assert master_response == slave_response

    # test the default handlers
    assert net.null() == 'NULL'
    assert master.pass_through(master.get_flag('NULL')) == 'NULL'
    assert master.null() == "NULL"
    assert slave.null() == "NULL"

    try:
        slave.force_error()
    except Exception:
        if "RemoteError" not in traceback.format_exc():
            pytest.fail("Remote Exception failure")


def test_subscriptions(peers):
    master, slave = peers

    test_message = "my message"

    @net.subscribe('my_event', peers=slave)
    def handle_subscribe(message):
        assert test_message == message

    @net.event('my_event')
    def my_event(*args, **kwargs):
        assert args[0] == test_message
        return args, kwargs

    my_event(test_message)


def test_peer_handle(peers):
    """
    Tests that the peer is handling incoming requests correctly.
    """
    master, slave = peers

    try:
        master.execute(slave, 'missing_connection', (), {})
        pytest.fail('Invalid connection is not being handled correctly.')
    except Exception:
        assert "Peer does not have the connection you are requesting" in traceback.format_exc()


def test_api():
    """
    Test api functions
    """
    net.LOGGER.debug("Test Header")

    # test peer look up
    net.peers()
    net.peers(groups=['group1'], refresh=True)
    net.peers(on_host=True, refresh=True)
    net.peer_group()

    # test non-threaded
    net.THREAD_LIMIT = 0

    net.peers()
    net.peers(groups=['group1'], refresh=True)
    net.peers(on_host=True, refresh=True)
    net.peer_group()
