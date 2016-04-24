import pytest
from pydrill.client import PyDrill


@pytest.fixture(scope='function', autouse=True)
def pydrill_instance():
    drill = PyDrill()
    return drill


@pytest.fixture()
def pydrill_url(pydrill_instance):
    """
    :type pydrill_instance: pydrill.client.PyDrill
    """
    return pydrill_instance.transport.connection.base_url
