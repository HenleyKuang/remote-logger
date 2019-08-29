"""
:author: Henley Kuang
:since: 08/14/2019
"""
import logging
import pytest

from remote_logger.clients.sentry_logger_client import SentryLoggerClient
from remote_logger.clients.stackdriver_logger_client import StackdriverLoggerClient
from remote_logger.remote_logger_handler import RemoteLoggerHandler
from remote_logger.util.excepts import (
    InvalidClientTypeException,
)


def test_initialize_sentry_logger_handler():
    """
    Test initialization of sentry logger handler
    """
    try:
        sentry_client = SentryLoggerClient(dsn="https://test@sentry.io/1")
        RemoteLoggerHandler(client=sentry_client)
    except Exception as e:
        pytest.fail("Exception raised: %s" % e)


def test_initialize_stackdriver_logger_handler():
    """
    Test initialization of sentry logger handler
    """
    try:
        stackdriver_client = StackdriverLoggerClient()
        RemoteLoggerHandler(client=stackdriver_client)
    except Exception as e:
        pytest.fail("Exception raised: %s" % e)


def test_initialize_stackdriver_with_error_repoting_level_logger_handler():
    """
    Test initialization of sentry logger handler
    """
    try:
        stackdriver_client = StackdriverLoggerClient(
            error_reporting_level=logging.ERROR)
        RemoteLoggerHandler(client=stackdriver_client)
    except Exception as e:
        pytest.fail("Exception raised: %s" % e)


def test_initialize_invalid_client_type_logger_handler():
    """
    Test initialization of an invalid client_type
    """
    with pytest.raises(InvalidClientTypeException):
        RemoteLoggerHandler("this should fail")
