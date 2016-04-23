#!/usr/bin/env python
# -*- coding: utf-8 -*-


def test_plan_for_select_employee_mocked(pydrill_instance):
    sql = "SELECT * FROM cp.`employee.json` ORDER BY salary DESC LIMIT 1"
    result = pydrill_instance.plan(sql=sql)
    assert result.response.status_code == 200
