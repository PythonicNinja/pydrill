#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pydrill.client.result import Stats, Result, Drillbit


def test_stats(pydrill_instance):
    """
    :type pydrill_instance: pydrill.client.PyDrill
    """
    stats = pydrill_instance.stats()
    assert type(stats) == Stats
    assert stats.response.status_code == 200
    assert stats.max_direct_memory

    assert stats.control_port_address
    assert stats.user_port_address
    assert stats.data_port_address

    assert stats.drillbits_number
    assert type(stats.drillbits) == type([])
    assert type(stats.drillbits[0]) == Drillbit


def test_metrics(pydrill_instance):
    """
    :type pydrill_instance: pydrill.client.PyDrill
    """
    result = pydrill_instance.metrics()
    assert type(result) == Result
    assert result.response.status_code == 200
    assert 'gauges' in result.data.keys()
