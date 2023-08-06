"""
Module to handle basic session
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import socket
import time
import os

from ssh2.session import Session as Ssh2Session  # pylint: disable=E0611
from ssh2.utils import wait_socket  # pylint: disable=E0611
from ssh2.exceptions import AuthenticationError, SocketDisconnectError, SocketRecvError  # pylint: disable=E0611
from netssh2 import log
from netssh2.exceptions import (
    NetSsh2Timeout,
    NetSsh2ChannelException,
    NetSsh2TooManyRetriesException,
    NetSsh2AuthenticationError,
    NetSsh2HostError
)
from netssh2.globals import LIBSSH2_ERROR_EAGAIN
from netssh2 import set_logging_level


class Session(object):  # pylint: disable=R0902
    """
    Defines default session to be used across multiple vendors.
    """

    def __init__(  # pylint: disable=R0913,R0914
            self,
            host="",
            user="",
            passwd="",
            key_file_private=None,
            key_file_public=None,
            key_passwd="",
            port=22,
            timeout=5000,
            buffer_size=1024,
            target_buffer_size=1024,
            auth_retries=5,
            auth_delay=2000,
            socket_retries=100,
            socket_delay=100,
            prompt=None,  # TODO: Add automatic prompt detection
            command_prompt=None,
            header_newline=True,
            newline="\n",  # TODO: Add automatic newline chars detection (can be \r\r\n for example)
            invoke_shell=False,
            verbose=True,
            logging_level="INFO"
    ):
        """

        :param host: host address to connect to
        :type host: string

        :param user: username for authentication
        :type user: string

        :param passwd: password for authentication
        :type passwd: string

        :param key_file_private: path to private key file
        :type key_file_private: string

        :param key_file_public: path to public key file. Not required if using same location as private (private.pub)
        :type key_file_public: string

        :param key_passwd: password for private key unlocking, default ""
        :type key_passwd: string

        :param port: port number, default 22
        :type port: int

        :param timeout: timeout in miliseconds
        :type timeout: int

        :param buffer_size: Size of buffer to read at once every iteration, default 1024
        :type buffer_size: int

        :param target_buffer_size: Some devices allow only limited length of command, default 1024
        :type target_buffer_size: int

        :param auth_retries: number of retries for authentication
        :type auth_retries: int

        :param auth_delay: delay in miliseconds between authentication retries
        :type auth_delay: int

        :param socket_retries: number of retries for socket connection
        :type socket_retries: int

        :param socket_delay: delay in miliseconds between socket retries
        :type socket_delay: int

        :param prompt: commandline prompt to wait for with interactive shell
        :type prompt: string

        :param command_prompt: sometimes the prompt changes when command is issued, pass it here
        :type command_prompt: string

        :param header_newline: With invoke shell do we need to send newline at the beginning to trigger 1st prompt?
        :type header_newline: bool

        :param newline: newline characters to confirm command, default \n
        :type newline: string

        :param invoke_shell: should we invoke interactive shell? default False
        :type invoke_shell: bool

        :param verbose: be verbose, print stuff from time to time, default True
        :type verbose: bool

        :param logging_level: Specify logging level, default INFO
        :type logging_level: string
        """
        self.host = host
        self.user = user
        self.passwd = passwd
        self.key_file_private = key_file_private
        self.key_file_public = key_file_public
        self.key_passwd = key_passwd
        self.port = port

        self.verbose = verbose
        self.logging_level = logging_level
        set_logging_level(self.logging_level)

        # set timeout
        self.timeout = self._limit_timeout_value(int(timeout))

        self.buff_size = buffer_size
        self.target_buff_size = target_buffer_size
        self.auth_retries = auth_retries
        self.auth_delay = auth_delay
        self.socket_retries = socket_retries
        self.socket_delay = socket_delay
        self.prompt = prompt
        self.command_prompt = command_prompt or prompt
        self.header_newline = header_newline
        self.newline = newline
        self.invoke_shell = invoke_shell

        self.sock = None
        self.session = None
        self.chan = None

        self.stdout = ""
        self.stdout_buff = ""
        self.stderr = ""
        self.stderr_buff = ""

        self.create_session()

    def set_timeout(self, new_timeout):
        """
        Setting different timeout with opened session.
        :param new_timeout: New timeout value in miliseconds.
        :type new_timeout: int

        :return: True
        :rtype: bool
        """
        assert isinstance(new_timeout, int), "New timeout is not int."
        assert self.session, "Session is not created"
        self.timeout = self._limit_timeout_value(new_timeout)
        self.session.set_timeout(self.timeout)
        return True

    def set_prompt(self, new_prompt):
        """
        Setting different prompt with opened session.
        :param new_prompt: new string to wait for after command with invoke_shell
        :type new_prompt: string

        :return: True
        :rtype: bool
        """
        assert isinstance(new_prompt, type("")), "New prompt is not string."
        if self.prompt == self.command_prompt:
            self.command_prompt = new_prompt
        self.prompt = new_prompt
        return True

    @staticmethod
    def _limit_timeout_value(timeout):
        """
        This prevents from overflowing C long int
        :param timeout: timeout value
        :type timeout: int

        :return: timeout value that fits C long int
        :rtype: int
        """
        return timeout if timeout <= 2 ** 32 else 2 ** 32

    def _connect_socket(self, try_number=1):
        """
        This function is to handle socket errors and disconnections.
        When we get them, we need to start the whole socket operation again.
        logging.debug any socket exceptions.
        :param try_number:
        :type try_number:

        :raises:  netssh2.exceptions.NetSsh2TooManyRetriesException if socket_retries number is exceeded.
        :raises:  netssh2.exceptions.NetSsh2HostError when given invalid/unreachable host

        :return: True
        :rtype: bool
        """

        def _retry(_try_number):
            # Try again after some delay
            time.sleep(float(self.socket_delay) / 1000)
            return self._connect_socket(_try_number + 1)

        log.debug("Connecting socket")
        assert isinstance(self.socket_retries, int), "socket_retries is not int"
        assert isinstance(self.host, type("")), "host is not string"
        assert isinstance(self.port, int), "port is not it"
        assert isinstance(self.timeout, (float, int)), "timout is not either float or int"

        if try_number == self.socket_retries + 1:
            raise NetSsh2TooManyRetriesException("Could not establish socket connection after %s tries."
                                                 % self.socket_retries)
        try:
            # Create socket connection
            socket_connection = socket.create_connection((self.host, self.port), float(self.timeout) / 1000)
            # Create a session
            self.session = Ssh2Session()
            self.session.handshake(socket_connection)
        except SocketDisconnectError:
            log.debug("Got SocketDisconnectError, trying to connect to socket again after delay. %s/%s",
                      try_number,
                      self.socket_retries)
            return _retry(try_number)
        except socket.gaierror:
            raise NetSsh2HostError("Name or service '%s' not known" % self.host)
        except socket.timeout:
            log.debug("Connecting to socket timed out after %s miliseconds.", self.timeout)
            raise NetSsh2Timeout("Connecting to host '%s' timed out after %s miliseconds" % (self.host, self.timeout))
        except socket.error as exception:
            log.debug("Got socket.error: '%s', retrying connection to socket after delay. %s/%s", exception,
                      try_number, self.socket_retries)
            return _retry(try_number)

        log.debug("Socket connected")
        return True

    def authenticate_session(self):
        """
        Tries to authenticate existing session

        :raises:  netssh2.exceptions.NetSsh2AuthenticationError when authentication fails
        :raises:  netssh2.exceptions.NetSsh2TooManyRetriesException if number of auth_retries is exceeded
        :raises:  netssh2.exceptions.Exception if any other issue happens when authenticating

        :return: True
        :rtype: bool
        """
        log.debug("Starting to authenticate session")
        assert self.user, "user is not set"
        assert isinstance(self.user, type("")), "user is not string"
        assert self.session, "session is not created"
        assert isinstance(self.auth_retries, int), "auth_restries is not int"

        i = 0
        while True:
            # Try to authenticate user
            try:
                if self.key_file_private:
                    # Authenticating using private key in file
                    assert isinstance(self.key_file_private, type("")), "private key must be string"
                    assert os.path.isfile(self.key_file_private), "private key file dost not exist"
                    if not self.key_file_public and os.path.isfile(self.key_file_private + ".pub"):
                        self.key_file_public = self.key_file_private + ".pub"
                    assert isinstance(self.key_file_public, type("")), "public key must be string"
                    assert os.path.isfile(self.key_file_public), "public key file dost not exist"
                    assert isinstance(self.key_passwd, type("")), "private key password must be string"
                    self.session.userauth_publickey_fromfile(self.user, self.key_file_private,
                                                             publickey=self.key_file_public, passphrase=self.key_passwd)
                else:
                    # Authenticating using user and password
                    self.session.userauth_password(self.user, self.passwd)
                break
            except AuthenticationError:
                raise NetSsh2AuthenticationError("Authentication failed when connecting to %s" % self.host)
            except (ValueError, OSError):
                log.info("Could not SSH to %s, waiting for it to start", self.host)
                i += 1
            except SocketDisconnectError:
                log.info("Socket got disconnected in between, connecting again.")
                self._connect_socket()
                i += 1
            except Exception as exception:
                log.error("Could not SSH to %s", self.host)
                log.debug("Exception: %s", exception)
                raise
            # If we could not connect within set number of tries
            if i == self.auth_retries:
                raise NetSsh2TooManyRetriesException("Could not connect to %s after %s retries. Giving up"
                                                     % (self.auth_retries, self.host))
            # Wait before next attempt
            time.sleep(float(self.auth_delay) / 1000)
        log.debug("Session authenticated")
        return True

    def create_session(self):
        """
        Connect to a host using ssh
        :return: True
        :rtype: bool
        """
        self._connect_socket()
        self.authenticate_session()
        self.configure_session()
        return True

    def disconnect(self):
        """
        Disconnect from a ssh session
        :return: True
        :rtype: bool
        """
        self.session.disconnect()

        # Clean up
        self.chan = None
        self.sock = None
        self.session = None
        return True

    def configure_session(self):
        """
        Sets up nonblocking mode, which allows to wait for socket to be ready and more control over channel.
        :return: True
        :rtype: bool
        """
        log.debug("Configuring session")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.session.set_blocking(False)

        assert isinstance(self.timeout, int), "timeout is not int"
        self.session.set_timeout(self.timeout)

        log.debug("Session configured")
        return True

    def open_channel(self):
        """
        Opens channel on ssh2 session.
        :raises:  netssh2.exceptions.NetSsh2ChannelException if the channel is not available for some reason.

        :return: True
        :rtype: bool
        """
        log.debug("Openning new channel.")
        self.chan = self._execute_function(self.session.open_session)
        if not self.chan:
            raise NetSsh2ChannelException("Could not open channel.")
        log.debug("Channel opened.")
        return True

    def clean_shell_header(self):
        """
        Gets rid of interactive shell header.
        :raises:  netssh2.exceptions.NetSsh2Timeout in case of timeout when reading the channel.

        :return: True
        :rtype: bool
        """
        if self.prompt:
            self._clear_buffers()
            # Be sure to get prompt
            assert self.newline, "newline char is not set"
            assert isinstance(self.header_newline, bool), "header_newline is not bool"
            if self.header_newline:
                self._write(self.newline)  # TODO: Prompt detection here
            # wait for prompt
            assert isinstance(self.stdout_buff, type("")), "stdout_buff is not string"
            while self.prompt not in self.stdout_buff:
                try:
                    _, resp = self.read_chan(buff_size=9999)
                except NetSsh2Timeout:
                    log.error("Waiting for prompt '%s' timed out after %s ms.", self.prompt, self.timeout)
                    log.debug("DEBUG: Got this output: \n %s", self._encode_to_bytes(self.stdout_buff))
                    resp = self.prompt
                self.stdout_buff += self._decode_from_bytes(resp)

        else:
            # get rid of the whole header
            self._execute_function(self.chan.read, size=65535)
        return True

    def configure_channel(self):
        """
        Does any channel configuration, for example invoking interactive shell if invoke_shell=True.
        :return: True
        :rtype: bool
        """
        log.debug("Configuring channel.")
        if self.invoke_shell:
            # Make this interactive shell
            assert self.chan, "chan (channel) is not created/open"
            self._execute_function(self.chan.pty)
            self._execute_function(self.chan.shell)
            self.clean_shell_header()
        log.debug("Channel configured.")
        return True

    def read_chan(self, buff_size=None, stderr=False):
        """
        Read channel output in non blocking way.
        :param buff_size: Buffer size to read from the channel
        :type buff_size: int

        :param stderr: Do we want to read STDERR (True) instead of STDOUT (False)?
        :type stderr: bool

        :raises:  netssh2.exceptions.NetSsh2Timeout in case of timeout when reading channel.

        :return: (size, buffer) size and payload read from the channel
        :rtype: tuple(int, str)
        """
        buff_size = buff_size or self.buff_size
        assert self.chan, "chan (channel) is not created/open"
        func = self.chan.read
        if stderr:
            func = self.chan.read_stderr
        size, tmp_buf = func(buff_size)
        assert isinstance(self.timeout, (int, float)), "timeout is not either float or int"
        time_end = time.time() + float(self.timeout) / 1000
        while size == LIBSSH2_ERROR_EAGAIN:
            wait_socket(self.sock, self.session, timeout=int(float(self.timeout) / 1000))
            size, tmp_buf = func(buff_size)
            if time.time() > time_end:
                raise NetSsh2Timeout
        return size, tmp_buf

    def _execute_function(self, func, **kwargs):
        """
        Executes any ssh function when the socket is not blocked (LIBSSH2_ERROR_EAGAIN)
        :param func: pointer to function to be executed
        :type func: function

        :param kwargs: any kwargs to be passed to the function

        :return: Anything the function returns
        :rtype: type(ret of function)
        """
        ret = func(**kwargs)
        time_end = time.time() + float(self.timeout) / 1000
        while ret == LIBSSH2_ERROR_EAGAIN:
            wait_socket(self.sock, self.session, float(self.timeout) / 1000)
            ret = func(**kwargs)
            if time.time() > time_end:
                raise NetSsh2Timeout
        return ret

    def _execute(self, command):
        """
        Wrapper for chan.execute to take keyword argument
        :param command: command to execute on the channel
        :type command: string

        :return: output of ssh2.channel.execute
        :rtype: int
        """
        assert self.chan, "chan (channel) is not created/open"
        return self.chan.execute(command)

    def _write(self, buff):
        """
        Wrapper for chan.write to take keyword argument
        :param buff: command to execute on the channel
        :type buff: string

        :return: output of ssh2.channel.write
        :rtype: int
        """
        assert self.chan, "chan (channel) is not created/open"
        return self.chan.write(buff)

    def _clear_buffers(self):
        """
        Clears internal buffers for channel reading
        :return: True
        :rtype: bool
        """
        self.stdout = ""
        self.stderr = ""
        self.stdout_buff = ""
        self.stderr_buff = ""
        return True

    def read_stdout(self):
        """
        Reads 1024 chars from channel STDOUT.
        :return: size of buffer that was read
        :rtype: int
        """
        size, self.stdout_buff = self.read_chan(buff_size=self.buff_size)
        self.stdout += self._decode_from_bytes(self.stdout_buff)
        return size

    def read_stderr(self):
        """
        Reads 1024 chars from channel STDERR.
        :return: size of buffer that was read
        :rtype: int
        """
        size, self.stderr_buff = self.read_chan(buff_size=self.buff_size)
        self.stderr += self._decode_from_bytes(self.stderr_buff)
        return size

    def _split_data_to_fit_buffer(self, data):
        if len(data) > self.target_buff_size:
            assert isinstance(self.target_buff_size, int), "Target buffer size mut be integer."
            assert self.target_buff_size > 0, "Target buffer size must be > 0."
            data = [data[i:i + self.target_buff_size] for i in range(0, len(data), self.target_buff_size)]
            log.debug("Data was too long for target buffer, split into: '%s'", data)
            return data
        return [data]

    def send_cmd(self, cmd):
        """
        Sends command over ssh2 channel.
        :param cmd: command to send
        :type cmd: string

        :raises:  netssh2.exceptions.NetSsh2Timeout in case of timeout

        :return: True
        :rtype: bool
        """
        log.debug("Starting to send command '%s'.", cmd)
        assert isinstance(cmd, type("")), "cmd (command) is not string"
        assert self.chan, "chan (channel) is not created/open"

        if self.verbose:
            log.info("Running ssh command '%s'", cmd)

        if self.invoke_shell:
            # send command with newline symbol
            cmd = self._split_data_to_fit_buffer(cmd + self.newline)
            for cmd_part in cmd:
                self._write(cmd_part)
        else:
            try:
                self._execute_function(self._execute, command=cmd)
            except NetSsh2Timeout:
                log.debug("Closing channel")
                self._execute_function(self.chan.close)
                raise NetSsh2Timeout("ssh - Got timeout (%s ms) while executing command: '%s'" % (self.timeout, cmd))
            except Exception as exception:
                log.error("ssh - Could not execute command: '%s'", cmd)
                log.error("Failed due: %s", repr(exception))
                log.debug("Closing channel")
                self._execute_function(self.chan.close)
                raise
        log.debug("Command sent.")
        return True

    @staticmethod
    def _decode_from_bytes(string):
        """
        Tries to decode any string from bytes. Does not fail if gets already decoded string.
        :param string: string to decode
        :type string: bytes
        :return: decoded string
        :rtype: basestring
        """
        return string if isinstance(string, type("")) else string.decode('ascii', 'ignore')

    @staticmethod
    def _encode_to_bytes(string):
        """
        Tries to encode any string from bytes. Does not fail if gets already encoded string.
        :param string: string to encode
        :type string: basestring
        :return: encoded string
        :rtype: bytes
        """
        return string if isinstance(string, bytes) else string.encode('ascii', 'ignore')

    def read_until_prompt(self):
        """
        Keep reading channel until we get prompt.
        :return: True
        :rtype: bool
        """
        log.debug("Reading until we get prompt.")
        # read until we get prompt again
        while not (self.stdout.endswith(self.command_prompt) or self.stdout.endswith(self.prompt)):
            try:
                _, self.stdout_buff = self.read_chan(buff_size=self.buff_size)
            except NetSsh2Timeout:
                log.error("Reading STDOUT timed out after %s ms, did not get prompt '%s'.", self.timeout,
                          self.command_prompt)
                log.debug("DEBUG: Got this output: \n %s", self._encode_to_bytes(self.stdout_buff))
                self.stdout_buff = self.command_prompt
            self.stdout += self._decode_from_bytes(self.stdout_buff)
        # Add newline at the end to prevent the above while condition to be True before reading some data
        self.stdout += "\n"
        log.debug("Reading complete.")
        return True

    def read_output(self):
        """
        Reads output of the command we sent.
        :return: True
        :rtype: bool
        """
        log.debug("Reading output.")
        # If there is prompt, we have to wait for it before being able to read the channel
        if self.prompt:
            self.read_until_prompt()
        else:
            # Read until we do not receive more bytes. First STDOUT, than STDERR
            log.debug("Reading STDOUT.")
            size = 1
            while size > 0:
                try:
                    size = self.read_stdout()
                except NetSsh2Timeout:
                    log.error("Reading STDOUT ssh channel timed out after %s ms.", self.timeout)
                    size, self.stdout_buff = (0, "")
            log.debug("Reading STDERR.")
            size = 1
            while size > 0:
                try:
                    size = self.read_stderr()
                except NetSsh2Timeout:
                    log.warning("Reading STDERR ssh channel timed out after %s ms.", self.timeout)
                    size, self.stderr_buff = (0, "")
            log.debug("Reading complete")
        return True

    def close_channel(self, keep_alive=False):
        """
        Closes channel and returns exist status.
        :param keep_alive: Should we keep the channel open and just get exist status? default False
        :type keep_alive: bool
        :return: channel exit status
        :rtype: int
        """
        if not keep_alive:
            log.debug("Closing channel")
            self._execute_function(self.chan.close)
        log.debug("Getting exit status.")
        return self._execute_function(self.chan.get_exit_status)

    def run_cmd(self, cmd, return_output=False):
        """
        Run a command to a specific ssh session
        :param cmd: command to run over ssh
        :type cmd: string

        :param return_output: Should we return also output
        :type return_output: bool

        :return: exit_status of command or (exit_status, output) in case of return_output=True
        :rtype: int or tuple(int, str)
        """

        def _get_channel():
            """
            With invoke_shell we want single channel, otherwise send command on new channel every time
            """
            if self.chan and self.invoke_shell:
                return
            self.open_channel()
            self.configure_channel()

        self._clear_buffers()

        _get_channel()

        self.send_cmd(cmd)
        try:
            self.read_output()
        except SocketRecvError:
            # Socket was closed, this happens when for example we reboot the server by this command
            log.debug("Got SocketRecvError, connection was closed by server.")

        log.debug("STDOUT: '%s'", self.stdout)
        # With invoke shell these are merged already
        if not self.invoke_shell:
            # merge STDOUT and STDERR
            log.debug("STDERR: '%s'", self.stderr)
            log.debug("Merging STDOUT and STDERR")
            self.stdout += self.stderr

        if self.verbose:
            print(self.stdout)

        # Close channel at the end
        exit_status = self.close_channel(keep_alive=self.invoke_shell)

        log.debug("Running command complete.")
        if return_output:
            return exit_status, self.stdout

        return exit_status

    def send_scp(self, source_file, destination_path):
        """
        Send file over SCP.
        :param source_file: Path to source file
        :type source_file: string
        :param destination_path: Path on server to copy file to
        :type destination_path: string
        :return: exist status
        :rtype: string
        """
        file_info = os.stat(source_file)

        log.debug("Initializing SCP send.")
        self.chan = self._execute_function(self.session.scp_send64, path=destination_path,
                                           mode=file_info.st_mode & 0o777, size=file_info.st_size,
                                           mtime=file_info.st_mtime, atime=file_info.st_atime)
        log.debug("Starting SCP send.")
        with open(source_file, 'rb') as local_fh:
            for data in local_fh:
                for data_part in self._split_data_to_fit_buffer(data):
                    self._write(data_part)
        log.debug("Data sent.")

        return self.close_channel()
