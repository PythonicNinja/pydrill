#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
import responses
from pydrill.client import PyDrill
from pydrill.exceptions import TransportError


@responses.activate
def test_authentication_success(pydrill_url):
    responses.add(**{
        'method': responses.POST,
        'url': "{0}/{1}".format(pydrill_url, '/j_security_check'),
        'status': 200,
    })

    PyDrill(auth='user:password')


@responses.activate
def test_authentication_failure(pydrill_url):
    responses.add(**{
        'method': responses.POST,
        'url': "{0}/{1}".format(pydrill_url, '/j_security_check'),
        'content_type': 'text/html',
        'status': 200,
    })

    with pytest.raises(TransportError):
        PyDrill(auth='user:password')
