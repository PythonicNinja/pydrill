#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
import responses

from pydrill.client.result import Result


def test_storage(pydrill_instance):
    """
    :type pydrill_instance: pydrill.client.PyDrill
    """
    result = pydrill_instance.storage()
    assert type(result) == Result
    assert result.response.status_code == 200


@pytest.mark.parametrize('name', [
    'mongo', 'hive', 'cp', 'json', 'dfs', 's3', 'kudu', 'hbase'
])
def test_storage_detail(pydrill_instance, name):
    """
    :type pydrill_instance: pydrill.client.PyDrill
    """
    result = pydrill_instance.storage_detail(name=name)
    assert type(result) == Result
    assert result.response.status_code == 200


@pytest.mark.parametrize('name', [
    'mongo', 'hive', 'cp', 'json', 'dfs', 's3', 'kudu', 'hbase'
])
@pytest.mark.parametrize('value', [
    False, True
])
@responses.activate
def test_storage_enable(pydrill_instance, pydrill_url, name, value):
    """
    :type pydrill_instance: pydrill.client.PyDrill
    """
    responses.add(**{
        'method': responses.GET,
        'url': '{0}/{1}'.format(pydrill_url, 'storage/{0}/enable/{1}'.format(name, 'true' if value else 'false')),
        'content_type': 'application/json',
        'status': 200,
    })
    result = pydrill_instance.storage_enable(name=name, value=value)
    assert type(result) == Result
    assert result.response.status_code == 200


@pytest.mark.parametrize('name', [
    'mongo', 'hive', 'cp', 'dfs', 's3', 'kudu', 'hbase'
])
def test_storage_update(pydrill_instance, name):
    """
    :type pydrill_instance: pydrill.client.PyDrill
    """
    result = pydrill_instance.storage_detail(name=name)
    result = pydrill_instance.storage_update(name=name, config=result.data)
    assert type(result) == Result
    assert result.response.status_code == 200


@pytest.mark.parametrize('name', [
    'mongo', 'hive', 'cp', 'json', 'dfs', 's3', 'kudu', 'hbase'
])
@responses.activate
def test_storage_delete(pydrill_instance, pydrill_url, name):
    """
    :type pydrill_instance: pydrill.client.PyDrill
    """
    responses.add(**{
        'method': responses.DELETE,
        'url': '{0}/{1}'.format(pydrill_url, 'storage/{0}.json'.format(name)),
        'content_type': 'application/json',
        'status': 200,
    })
    result = pydrill_instance.storage_delete(name=name)
    assert type(result) == Result
    assert result.response.status_code == 200
