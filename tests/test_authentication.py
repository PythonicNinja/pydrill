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
        'url': "{0}/{1}".format(pydrill_url, 'j_security_check'),
    })

    PyDrill(auth='user:password')


@responses.activate
def test_authentication_failure():
    with pytest.raises(TransportError):
        PyDrill(auth='user:password')
