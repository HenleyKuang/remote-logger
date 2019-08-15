"""
:author: Henley Kuang
:since: 08/14/2019
"""
import pytest

from remote_logger.remote_logger_handler import RemoteLoggerHandler
from remote_logger.util.definitions import (
    SENTRY,
    STACKDRIVER,
)
from remote_logger.util.excepts import (
    InvalidClientTypeException,
)


def test_initialize_sentry_logger_handler():
    """
    Test initialization of sentry logger handler
    """
    try:
        RemoteLoggerHandler(SENTRY,
                            dsn="https://test@sentry.io/1")
    except Exception as e:
        pytest.fail("Exception raised: %s" % e)


def test_initialize_stackdriver_logger_handler():
    """
    Test initialization of sentry logger handler
    """
    try:
        RemoteLoggerHandler(STACKDRIVER)
    except Exception as e:
        pytest.fail("Exception raised: %s" % e)


def test_initialize_invalid_client_type_logger_handler():
    """
    Test initialization of an invalid client_type
    """
    with pytest.raises(InvalidClientTypeException):
        RemoteLoggerHandler("this should fail")
