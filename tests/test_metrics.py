#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pydrill_setup
----------------------------------

Tests for `pydrill` metrics function.
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

    #The values of the metrics will differ from machine to machine, so basically
    #just testing that it works.
    def test_metrics(self):
        metrics = self.drill.metrics()
        assert len( metrics.data ) == 6
        assert metrics.number_of_drill_bits >= 1
        assert isinstance( metrics.max_direct_memory, int )


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())


