#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pydrill_setup
----------------------------------

Tests for `pydrill` module.
Related to setup of :class:~`pydrill.PyDrill`.
"""

import unittest

from pydrill.client import PyDrill


class TestPydrill(unittest.TestCase):
    def setUp(self):
        self.drill = PyDrill(host='localhost', port=8047)

    def test_transport_host(self):
        assert self.drill.transport.host == 'localhost'

    def test_transport_port(self):
        assert self.drill.transport.port == 8047

    # TODO: create more tests checking other params.

if __name__ == '__main__':
    import sys

    sys.exit(unittest.main())
