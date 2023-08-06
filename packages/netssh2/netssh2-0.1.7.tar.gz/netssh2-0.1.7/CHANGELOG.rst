Changelog
=========

0.1.7 (2019-04-26)
------------------
- Make sure command timeout works.
- Add tests for logging.
- Allow to change logging level on Session init plus some more debug.
- Move away from unittest to pure py.test.
- Allow to use key authentication.
- Wrap channel.write for nonblocking transfer.
- Add scp_send.
- Split command to multiple if it is longer than target buffer.
- Add toggle for sending newline when getting rid of the header.

0.1.6 (2019-04-12)
------------------
- Allow session with no pass.
- Allow to specify read buffer size.
- Add message level to log message.
- No need to merge STDOUT and STDERR with invoke shell.
- Add lots of debug messages for easier debugging.
- Add debug on SocketRecvError.
- Wrap encoding and decoding of strings to functions.
- Do not retry socket connection if we got timeout.
- Print output to debug on timeout when waiting for prompt.

0.1.5 (2019-04-02)
------------------
- Allow changing logging level on the run.
- Fix getting output from when running without interactive shell.

0.1.4 (2019-03-27)
------------------
- Upload to PyPi if pipeline is passing.
- Run CI build job every time (has build checks).
- Fix tag message.
- Specify long_description_content_type in setup.py to avoid warns.
- Move pushing to PyPi to CI and add wheels.
- Add setup.cfg with wheel specs.

0.1.3 (2019-03-26)
------------------
- Push to pypi only when twine check passes.
- Use only subject of commit in changelog.
- Push also tags when bumping version.

0.1.2 (2019-03-26)
------------------
- Add automatic MANIFEST.in updating to bump_version.sh.
- Add manifest file to include everything to built packages.
- Add script for automated version bumping.
- Add .gitignore.

0.1.1 (2019-03-26)
------------------
- Fix date of 0.0.1 release.
- Fix docs link in README.
- Add changelog to documentation.
- Add license metadata setup.py.
- Add changelog to setup.py long description (pypi).
- Have only GPL v3 on PyPi.

0.1.0 (2019-03-26)
------------------
- Add changelog.
- Improve README.
- Add pypi identifiers to setup.py.
- Add RST docs to be generated with sphinx using 'make html'.
- Fix python envs in tox.
- Add code coverage to tox test.
- Change command prompt too if changing prompt of existing session.
- Add basic tests for tox.
- Cleanup when disconnecting.
- Add messages to assertions.
- Catch error when given invalid hostname.
- Add linting CI.

0.0.1 (2019-03-21)
------------------
- Basic implementation of netssh2 to work with paralel SSH and interactive shell.
- Add license.
- Initial commit.

