#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from pydrill.exceptions import QueryError, ImproperlyConfigured


def test_select_employee(pydrill_instance):
    """
    :type pydrill_instance: pydrill.client.PyDrill
    """
    sql = "SELECT * FROM cp.`employee.json` ORDER BY salary DESC LIMIT 1"
    expected_result = {'columns': ['birth_date', 'department_id', 'education_level', 'employee_id', 'first_name',
                                   'full_name', 'gender', 'hire_date', 'last_name', 'management_role', 'marital_status',
                                   'position_id', 'position_title', 'salary', 'store_id', 'supervisor_id'],
                       'rows': [{'last_name': 'Nowmer', 'marital_status': 'S', 'management_role': 'Senior Management',
                                 'store_id': '0', 'position_id': '1', 'birth_date': '1961-08-26',
                                 'education_level': 'Graduate Degree', 'gender': 'F', 'supervisor_id': '0',
                                 'salary': '80000.0', 'department_id': '1', 'position_title': 'President',
                                 'full_name': 'Sheri Nowmer', 'hire_date': '1994-12-01 00:00:00.0',
                                 'first_name': 'Sheri', 'employee_id': '1'}]}

    result = pydrill_instance.query(sql=sql)

    assert result.response.status_code == 200
    assert result.data == expected_result


def test_select_iterator(pydrill_instance):
    """
    :type pydrill_instance: pydrill.client.PyDrill
    """
    sql = "SELECT * FROM cp.`employee.json` ORDER BY salary DESC LIMIT 1"

    for row in pydrill_instance.query(sql=sql):
        assert type(row) is dict


def test_select_pandas(pydrill_instance):
    """
    :type pydrill_instance: pydrill.client.PyDrill
    """
    sql = "SELECT * FROM cp.`employee.json` ORDER BY salary DESC LIMIT 1"

    with pytest.raises(ImproperlyConfigured):
        df = pydrill_instance.query(sql=sql).to_dataframe()


def test_select_without_sql(pydrill_instance):
    """
    :type pydrill_instance: pydrill.client.PyDrill
    """
    sql = ""
    try:
        result = pydrill_instance.query(sql=sql)
    except QueryError as e:
        assert e


def test_plan_for_select_employee(pydrill_instance):
    """
    :type pydrill_instance: pydrill.client.PyDrill
    """
    sql = "SELECT * FROM cp.`employee.json` ORDER BY salary DESC LIMIT 1"
    result = pydrill_instance.plan(sql=sql)
    assert result.response.status_code == 200


# TODO: create more tests with other queries.
