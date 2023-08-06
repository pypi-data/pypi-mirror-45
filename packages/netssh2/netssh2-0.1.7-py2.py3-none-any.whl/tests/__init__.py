"""
Common functions and configs for all tests
"""

from __future__ import absolute_import, division, print_function, unicode_literals
from netssh2.session import Session


HOST = "test.rebex.net"
USER = "demo"
PASSWD = "password"

NEWLINE = "\r\n"
PROMPT = "$ "

COMMAND = "uname"
OUTPUT = "Rebex Virtual Shell"


def get_session(**kwargs):
    """
    Creates instance of netssh2.session.Session object
    :param kwargs: any kwargs to pass to Session

    :return: session
    :rtype: class <netssh2.session.Session>
    """
    return Session(**kwargs)
