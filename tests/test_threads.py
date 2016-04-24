#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pydrill.client.result import Result


def test_threads(pydrill_instance):
    """
    :type pydrill_instance: pydrill.client.PyDrill
    """
    threads = pydrill_instance.threads()
    assert type(threads) == Result
    assert threads.response.status_code == 200
    assert type(threads.data) == type(u"")
