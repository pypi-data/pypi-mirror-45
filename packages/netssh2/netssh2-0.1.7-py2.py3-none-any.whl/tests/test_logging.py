"""
Any logging tests.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import logging
from . import HOST, USER, PASSWD, COMMAND, get_session


def test_check_logging_level(caplog):
    """Tests default logging level"""
    caplog.set_level(logging.DEBUG)
    session = get_session(host=HOST, user=USER, passwd=PASSWD, verbose=True)
    assert session.run_cmd(COMMAND) == 0
    assert 'Running ssh command' in caplog.text
    assert 'DEBUG' not in caplog.text
    assert session.disconnect()


def test_change_logging_level(caplog):
    """Tests changing logging level to DEBUG"""
    caplog.set_level(logging.DEBUG)
    session = get_session(host=HOST, user=USER, passwd=PASSWD, logging_level="debug")
    assert session.disconnect()
    assert 'DEBUG' in caplog.text
