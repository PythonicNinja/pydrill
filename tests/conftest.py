import pytest
from pydrill.client import PyDrill


@pytest.fixture(scope='function', autouse=True)
def pydrill_instance():
    drill = PyDrill()
    return drill
