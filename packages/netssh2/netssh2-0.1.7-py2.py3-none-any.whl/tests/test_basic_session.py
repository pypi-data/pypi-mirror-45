"""
Basic sanity test for SSH connection.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import pytest
import netssh2.exceptions as ex
from . import HOST, USER, PASSWD, PROMPT, NEWLINE, COMMAND, OUTPUT, get_session


def test_blank_session():
    """Tests creating empty(default) session, should raise NetSsh2HostError exception"""
    with pytest.raises(ex.NetSsh2HostError):
        get_session()


def test_simple_ssh(basic_session_module):
    """Tests creating and communicating over simple SSH."""
    session = basic_session_module
    assert session.run_cmd(COMMAND) == 0
    assert OUTPUT in session.run_cmd(COMMAND, return_output=True)[1]


def test_invoke_shell_ssh():
    """Tests creating and communicating over simple SSH with invoke shell."""
    session = get_session(host=HOST, user=USER, passwd=PASSWD, invoke_shell=True, prompt=PROMPT, newline=NEWLINE)
    assert session is not None
    assert session.run_cmd(COMMAND) == 0
    assert OUTPUT in session.run_cmd(COMMAND, return_output=True)[1]
    assert session.disconnect()


def test_set_prompt(basic_session_function):
    """Tests setting prompt"""
    session = basic_session_function
    assert session.prompt is None
    session.set_prompt("test_prompt")
    assert session.prompt == "test_prompt"


def test_timeout_init():
    """Tests timeout on session instance creation"""
    with pytest.raises(ex.NetSsh2Timeout):
        get_session(host=HOST, user=USER, passwd=PASSWD, timeout=1)


def test_timeout_command(basic_session_function):
    """Tests timeout on sending command"""
    session = basic_session_function
    assert session.set_timeout(1)
    assert session.timeout == 1
    assert session.timeout == session.session.get_timeout()
    with pytest.raises(ex.NetSsh2Timeout):
        session.run_cmd(COMMAND)


def test_disconnect():
    """Tests authentication errors"""
    with pytest.raises(ex.NetSsh2AuthenticationError):
        get_session(host=HOST, user="wrong", passwd=PASSWD)
    with pytest.raises(ex.NetSsh2AuthenticationError):
        get_session(host=HOST, user=USER, passwd="wrong")


def test_socket_retry():
    """Tests correct exception for socket running out of tries"""
    with pytest.raises(ex.NetSsh2TooManyRetriesException):
        get_session(host=HOST, user=USER, passwd=PASSWD, socket_retries=0)


def test_small_buffer():
    """Tests splitting command to fit buffer"""
    session = get_session(host=HOST, user=USER, passwd=PASSWD, invoke_shell=True, prompt=PROMPT, newline=NEWLINE,
                          target_buffer_size=3)
    assert session is not None
    assert session.run_cmd(COMMAND) == 0
    assert OUTPUT in session.run_cmd(COMMAND, return_output=True)[1]
    assert session.disconnect()


def test_wrong_command_exit_code(basic_session_module):
    """Tests getting exit code on wrong command"""
    session = basic_session_module
    assert session.run_cmd("wrong_command") == 127
