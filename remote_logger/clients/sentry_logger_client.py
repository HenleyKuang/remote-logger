"""
:author: Henley Kuang
:since: 08/05/2019
"""
import logging
import sentry_sdk

from sentry_sdk import push_scope
from sentry_sdk.integrations.logging import LoggingIntegration

from remote_logger.clients.logger_client import LoggerClient
from remote_logger.util.excepts import FailTranslatingPythonLogLevelException

SENTRY_DISABLE_LOGGING_INTEGRATION = LoggingIntegration(
    level=logging.INFO,  # Capture logging level for breadcrumbs
    event_level=None  # Do not send any logs as events, this module will handle the log handler
)

PYTHON_TO_SENTRY_LOG_LEVELS = {
    'CRITICAL': 'fatal',
    'FATAL': 'fatal',
    'ERROR': 'error',
    'WARN': 'warning',
    'WARNING': 'warning',
    'INFO': 'info',
    'DEBUG': 'debug',
}


def get_sentry_log_level(python_log_level):
    try:
        return PYTHON_TO_SENTRY_LOG_LEVELS[python_log_level]
    except KeyError:
        raise FailTranslatingPythonLogLevelException(
            "Could not translate python log level %s to a sentry log level" % python_log_level)


def before_send(event, hint):
    # before_send is a hook for sentry to modify the event before sending
    try:
        group_id = event['extra']['group_id']
        # Modify the fingerprint to our error code to group Exceptions together
        event['fingerprint'] = [group_id]
    except KeyError:
        pass
    return event


class SentryLoggerClient(LoggerClient):

    def __init__(self, **kwargs):
        dsn = kwargs['dsn']
        sentry_sdk.init(dsn=dsn,
                        before_send=before_send,
                        integrations=[SENTRY_DISABLE_LOGGING_INTEGRATION])
        self._client = sentry_sdk

    def send_log(self, message, level, group_id, primary_metadata, secondary_metadata):
        sentry_log_level = get_sentry_log_level(level)
        with push_scope() as scope:
            scope.level = sentry_log_level
            for tag_name, tag_value in primary_metadata.items():
                scope.set_tag(tag_name, tag_value)
            for tag_name, tag_value in secondary_metadata.items():
                scope.set_extra(tag_name, tag_value)
            # if group_id is set, we'll pass it to extra
            if group_id is not None:
                # pass group_id to extra so before_send can grab it for fingerprinting
                scope.set_extra('group_id', group_id)
            self._client.capture_message(message)
