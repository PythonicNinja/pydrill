#!/usr/bin/env python
# -*- coding: utf-8 -*-
import responses
import uuid
from pydrill.client.result import Profiles, Result


def test_profiles(pydrill_instance):
    """
    :type pydrill_instance: pydrill.client.PyDrill
    """
    profiles = pydrill_instance.profiles()
    assert type(profiles) == Profiles
    assert profiles.response.status_code == 200
    assert type(profiles.running_queries) == type([])
    assert type(profiles.finished_queries) == type([])


@responses.activate
def test_profile(pydrill_instance, pydrill_url):
    """
    :type pydrill_instance: pydrill.client.PyDrill
    """
    query_id = uuid.uuid4()

    responses.add(**{
        'method': responses.GET,
        'url': "{0}/{1}".format(pydrill_url, 'profiles/{0}.json'.format(query_id)),
        'content_type': 'application/json',
        'status': 200,
    })

    result = pydrill_instance.profile(query_id=query_id)
    assert type(result) == Result
    assert result.response.status_code == 200


@responses.activate
def test_profile_cancel(pydrill_instance, pydrill_url):
    """
    :type pydrill_instance: pydrill.client.PyDrill
    """
    query_id = uuid.uuid4()

    responses.add(**{
        'method': responses.GET,
        'url': "{0}/{1}".format(pydrill_url, 'profiles/cancel/{0}'.format(query_id)),
        'content_type': 'application/json',
        'status': 200,
    })

    result = pydrill_instance.profile_cancel(query_id=query_id)
    assert type(result) == Result
    assert result.response.status_code == 200
