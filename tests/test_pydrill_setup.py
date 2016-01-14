#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pydrill_setup
----------------------------------

Tests for `pydrill` module.
Related to setup of :class:~`pydrill.PyDrill`.
"""

import unittest

import responses
from pydrill.client import PyDrill
from pydrill.exceptions import TransportError


class TestPydrill(unittest.TestCase):
    def setUp(self):
        self.drill = PyDrill(host='localhost', port=8047)

    def test_transport_host(self):
        assert self.drill.transport.host == 'localhost'

    def test_transport_port(self):
        assert self.drill.transport.port == 8047

    @responses.activate
    def test_is_active(self):
        responses.add(**{
            'method': responses.HEAD,
            'url': 'http://localhost:8047/',
            'status': 200,
            'content_type': 'application/json',
        })
        assert self.drill.is_active() == True

    @responses.activate
    def test_is_not_active_404(self):
        responses.add(**{
            'method': responses.HEAD,
            'url': 'http://localhost:8047/',
            'content_type': 'application/json',
            'status': 404,
        })
        assert self.drill.is_active() == False

    @responses.activate
    def test_is_not_active_500(self):
        responses.add(**{
            'method': responses.HEAD,
            'url': 'http://localhost:8047/',
            'content_type': 'application/json',
            'status': 500,
        })
        assert self.drill.is_active() == False

    @responses.activate
    def test_is_not_active_timeout(self):
        responses.add(**{
            'method': responses.HEAD,
            'url': 'http://localhost:8047/',
            'content_type': 'application/json',
            'status': 500,
        })
        try:
            self.drill.perform_request('HEAD', '/', params={'request_timeout': 0})
        except TransportError as e:
            assert e.status_code == e.args[0]
            assert e.error == e.args[1]
            assert e.info == e.args[2]
            assert str(e)
        else:
            assert False


    # TODO: create more tests checking other params.

if __name__ == '__main__':
    import sys

    sys.exit(unittest.main())
