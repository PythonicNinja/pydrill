#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import responses
from pydrill.exceptions import TransportError


def test_transport_host(pydrill_instance):
    """
    :type pydrill_instance: pydrill.client.PyDrill
    """
    assert pydrill_instance.transport.host == os.environ.get('PYDRILL_HOST', 'localhost')


def test_transport_port(pydrill_instance):
    """
    :type pydrill_instance: pydrill.client.PyDrill
    """
    assert pydrill_instance.transport.port == os.environ.get('PYDRILL_PORT', 8047)


def test_is_active(pydrill_instance):
    """
    :type pydrill_instance: pydrill.client.PyDrill
    """
    assert pydrill_instance.is_active() == True


@responses.activate
def test_is_not_active_404(pydrill_instance):
    """
    :type pydrill_instance: pydrill.client.PyDrill
    """
    responses.add(**{
        'method': responses.HEAD,
        'url': 'http://localhost:8047/',
        'content_type': 'application/json',
        'status': 404,
    })
    assert pydrill_instance.is_active() == False


@responses.activate
def test_is_not_active_500(pydrill_instance, pydrill_url):
    """
    :type pydrill_instance: pydrill.client.PyDrill
    """
    responses.add(**{
        'method': responses.HEAD,
        'url': pydrill_url,
        'content_type': 'application/json',
        'status': 500,
    })
    assert pydrill_instance.is_active() == False


@responses.activate
def test_is_not_active_201(pydrill_instance, pydrill_url):
    """
    :type pydrill_instance: pydrill.client.PyDrill
    """
    responses.add(**{
        'method': responses.HEAD,
        'url': pydrill_url,
        'content_type': 'application/json',
        'status': 201,
    })
    assert pydrill_instance.is_active() == False


def test_is_not_active_timeout(pydrill_instance):
    """
    :type pydrill_instance: pydrill.client.PyDrill
    """
    try:
        pydrill_instance.perform_request('HEAD', '/', params={'request_timeout': 0})
    except TransportError as e:
        assert e.status_code == e.args[0]
        assert e.error == e.args[1]
        assert e.info == e.args[2]
        assert str(e)
    else:
        assert False

# TODO: create more tests checking other params.
