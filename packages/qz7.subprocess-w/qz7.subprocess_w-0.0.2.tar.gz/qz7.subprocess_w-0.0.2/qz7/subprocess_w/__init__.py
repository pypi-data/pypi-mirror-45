"""
Subprocess wrapper

Proivdes a subclass of Popen,
that terminates gracefully instead of leaving zombie/orphan subprocesses.
"""

import logging
from subprocess import (Popen, TimeoutExpired)

log = logging.getLogger(__name__)

DEFAULT_WAIT_TIMEOUT = 0
DEFAULT_TERM_TIMEOUT = 30

def terminate_gracefully(process,
                         wait_timeout=DEFAULT_WAIT_TIMEOUT,
                         term_timeout=DEFAULT_TERM_TIMEOUT):
    """
    Terminate the process gracefully.
    """

    try:
        process.wait(timeout=wait_timeout)
    except TimeoutExpired:
        log.info("Terminating %d: %s", process.pid, process.args)
        try:
            process.terminate()
        except ProcessLookupError:
            return

        try:
            process.wait(timeout=term_timeout)
        except TimeoutExpired:
            log.warning("Killing %d: %s", process.pid, process.args)
            try:
                process.kill()
            except ProcessLookupError:
                return

            process.wait()

class PopenW(Popen):
    """
    Popen wrapper that exits gracefully.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        log.info("Starting %d: %s", self.pid, self.args)
        self._log_exited = True

    def is_dead(self):
        """
        Check and log if the process is dead.
        """

        if self.poll() is not None:
            if self._log_exited:
                log.info("Exited %d: %s", self.pid, self.args)
                self._log_exited = False

            return True

        return False

    def terminate_gracefully(self,
                             wait_timeout=DEFAULT_WAIT_TIMEOUT,
                             term_timeout=DEFAULT_TERM_TIMEOUT):
        """
        Terminate the process gracefully.
        """

        if self.is_dead():
            return

        terminate_gracefully(self, wait_timeout, term_timeout)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, value, traceback):
        self.terminate_gracefully()

    def __del__(self):
        self.terminate_gracefully()
