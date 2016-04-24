#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pydrill.client.result import Result


def test_options(pydrill_instance):
    """
    :type pydrill_instance: pydrill.client.PyDrill
    """
    threads = pydrill_instance.options()
    assert type(threads) == Result
    assert threads.response.status_code == 200
