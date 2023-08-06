# SPDX-License-Identifier: GPL-3.0-or-later

import contextlib
import logging
import subprocess


def configure_logging():

    stream_handler = logging.StreamHandler()
    stream_formatter = logging.Formatter(
        fmt="{levelname:8} {name:22} {message}", style="{"
    )
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(stream_formatter)

    file_handler = logging.FileHandler("debug.log", mode="w")
    file_formatter = logging.Formatter(
        fmt="{relativeCreated:7.0f} {levelname:8} {name:22} {message}",
        style="{",
    )
    file_handler.setFormatter(file_formatter)
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(stream_handler)
    root_logger.addHandler(file_handler)


def context_logger(name):

    logger = logging.getLogger(name)

    def log(description):
        logger.info(description + "...")
        try:
            yield
        except:
            logger.error(description + "... failed")
            raise
        else:
            logger.info(description + "... done")

    return contextlib.contextmanager(log)


class NonZeroExitCode(Exception):
    pass


def close_verbose_process(*, process, process_name, check=True, timeout):
    logger = logging.getLogger(__name__)

    try:
        stdout_data, stderr_data = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        logger.error(f"{process_name} is still running")
        with context_logger(__name__)(f"Kill {process_name}"):
            process.kill()
            stdout_data, stderr_data = process.communicate()

    for line in stdout_data.splitlines():
        logger.debug("< " + line)

    for line in stderr_data.splitlines():
        logger.error("< " + line)

    return_code = process.returncode

    if return_code >= 0:
        logger.debug(f"{process_name} exited with code {return_code}")
    else:
        logger.debug(
            f"{process_name} " f"was killed by signal {-1 * return_code}"
        )
    if check and return_code > 0:
        raise NonZeroExitCode(
            f"Process {process.args} exited with non-zero code {return_code}"
        )
    if check and return_code < 0:
        raise NonZeroExitCode(
            f"Process {process.args} was killed by signal {-1 * return_code}"
        )

    return return_code
