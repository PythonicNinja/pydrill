#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_select_queries_mocked
----------------------------------

Tests for `pydrill` module.
Related to select queries build with :class:~`pydrill.PyDrill`.
"""

import unittest

import responses

from pydrill.client import PyDrill
from pydrill.exceptions import QueryError


class TestPydrill(unittest.TestCase):
    def setUp(self):
        self.drill = PyDrill(host='localhost', port=8047)

    @responses.activate
    def test_select_employee_mocked(self):
        sql = "SELECT * FROM cp.`employee.json` ORDER BY salary DESC LIMIT 1"
        expected_result = {
            "columns": ["employee_id", "full_name", "first_name", "last_name", "position_id", "position_title",
                        "store_id", "department_id", "birth_date", "hire_date", "salary", "supervisor_id",
                        "education_level", "marital_status", "gender", "management_role"],
            "rows": [{
                "hire_date": "1994-12-01 00:00:00.0",
                "birth_date": "1961-08-26",
                "department_id": "1",
                "store_id": "0",
                "education_level": "Graduate Degree",
                "first_name": "Sheri",
                "position_id": "1",
                "management_role": "Senior Management",
                "last_name": "Nowmer",
                "gender": "F",
                "position_title": "President",
                "marital_status": "S",
                "salary": "80000.0",
                "employee_id": "1",
                "supervisor_id": "0",
                "full_name": "Sheri Nowmer"
            }]
        }

        responses.add(**{
            'method': responses.POST,
            'url': 'http://localhost:8047/query.json',
            'body': '{"queryType": "SQL","query": "%(sql)s"}' % ({'sql': sql}),
            'status': 200,
            'content_type': 'application/json',
            'json': expected_result,
        })

        result = self.drill.query(sql=sql)

        assert result.response.status_code == 200
        assert result.data == expected_result

    @responses.activate
    def test_select_iterator(self):
        sql = "SELECT * FROM cp.`employee.json` ORDER BY salary DESC LIMIT 1"
        expected_result = {
            "columns": ["employee_id", "full_name", "first_name", "last_name", "position_id", "position_title",
                        "store_id", "department_id", "birth_date", "hire_date", "salary", "supervisor_id",
                        "education_level", "marital_status", "gender", "management_role"],
            "rows": [{
                "hire_date": "1994-12-01 00:00:00.0",
                "birth_date": "1961-08-26",
                "department_id": "1",
                "store_id": "0",
                "education_level": "Graduate Degree",
                "first_name": "Sheri",
                "position_id": "1",
                "management_role": "Senior Management",
                "last_name": "Nowmer",
                "gender": "F",
                "position_title": "President",
                "marital_status": "S",
                "salary": "80000.0",
                "employee_id": "1",
                "supervisor_id": "0",
                "full_name": "Sheri Nowmer"
            }]
        }

        responses.add(**{
            'method': responses.POST,
            'url': 'http://localhost:8047/query.json',
            'body': '{"queryType": "SQL","query": "%(sql)s"}' % ({'sql': sql}),
            'status': 200,
            'content_type': 'application/json',
            'json': expected_result,
        })

        for row in self.drill.query(sql=sql):
            assert type(row) is dict

    def test_select_without_sql(self):
        sql = ""
        try:
            result = self.drill.query(sql=sql)
        except QueryError as e:
            assert e

    # TODO: create more tests with other queries.

if __name__ == '__main__':
    import sys

    sys.exit(unittest.main())
