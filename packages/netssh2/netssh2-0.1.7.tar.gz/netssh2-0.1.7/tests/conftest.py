"""
Common fixtures for all tests
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import pytest
from . import HOST, USER, PASSWD, get_session


def basic_session():
    """Creates basic SSH session"""
    session = get_session(host=HOST, user=USER, passwd=PASSWD)
    assert session is not None
    return session


@pytest.fixture(scope="module")
def basic_session_module():
    """Fixture for basic session on module scope"""
    session = basic_session()
    yield session
    assert session.disconnect()


@pytest.fixture(scope="function")
def basic_session_function():
    """Fixture for basic session on function scope"""
    session = basic_session()
    yield session
    assert session.disconnect()
