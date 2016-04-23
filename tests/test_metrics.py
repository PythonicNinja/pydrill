#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pydrill_setup
----------------------------------

Tests for `pydrill` module.
Related to select queries build with :class:~`pydrill.PyDrill`.
"""

import unittest

import responses

from pydrill.client import PyDrill


class TestPydrill(unittest.TestCase):
    def setUp(self):
        self.drill = PyDrill(host='localhost', port=8047)

    @responses.activate
    def test_select_employee_mocked(self):
        #sql = "SELECT * FROM cp.`employee.json` ORDER BY salary DESC LIMIT 1"
        expected_result = [{'name': 'Number of Drill Bits', 'value': 1}, {'name': 'Bit #0', 'value': 'osboxes initialized'}, {'name': 'Data Port Address', 'value': 'osboxes:31012'}, {'name': 'User Port Address', 'value': 'osboxes:31010'}, {'name': 'Control Port Address', 'value': 'osboxes:31011'}, {'name': 'Maximum Direct Memory', 'value': 8589934592}]
        

        responses.add(**{
            'method': responses.GET,
            'url': 'http://localhost:8047/stats.json',
            'status': 200,
            'content_type': 'application/json',
            'json': expected_result,
        })

        result = self.drill.metrics()

        assert result.response.status_code == 200
        assert result.data == expected_result
        assert len( result.data ) == 6
        assert result.number_of_drill_bits >= 1
        assert isinstance( result.max_direct_memory, int )
		
    # TODO: create more tests with other queries.

if __name__ == '__main__':
    import sys

    sys.exit(unittest.main())
