#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_plan_query_mocked
----------------------------------

Tests for `pydrill` module.
Related to plan select queries build with :class:~`pydrill.PyDrill`.
"""

import unittest

import responses

from pydrill.client import PyDrill


class TestPydrill(unittest.TestCase):
    def setUp(self):
        self.drill = PyDrill(host='localhost', port=8047)

    @responses.activate
    def test_plan_for_select_employee_mocked(self):
        sql = "SELECT * FROM cp.`employee.json` ORDER BY salary DESC LIMIT 1"

        responses.add(**{
            'method': responses.POST,
            'url': 'http://localhost:8047/query.json',
            'body': '{"queryType": "SQL","query": "explain plan for %(sql)s"}' % ({'sql': sql}),
            'status': 200,
            'content_type': 'application/json',
            'json': {},
        })

        result = self.drill.plan(sql=sql)
        assert result.response.status_code == 200


if __name__ == '__main__':
    import sys

    sys.exit(unittest.main())
