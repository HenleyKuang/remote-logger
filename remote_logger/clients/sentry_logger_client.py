"""
:author: Henley Kuang
:since: 08/05/2019
"""
import logging
import sentry_sdk

from sentry_sdk import push_scope
from sentry_sdk.integrations.logging import LoggingIntegration

from remote_logger.clients.logger_client import LoggerClient

SENTRY_DISABLE_LOGGING_INTEGRATION = LoggingIntegration(
    level=logging.INFO,  # Capture logging level for breadcrumbs
    event_level=None  # Do not send any logs as events, this module will handle the log handler
)


class SentryLoggerClient(LoggerClient):

    def __init__(self, **kwargs):
        dsn = kwargs['dsn']
        sentry_sdk.init(dsn=dsn,
                        integrations=[SENTRY_DISABLE_LOGGING_INTEGRATION])
        self._client = sentry_sdk

    def send_log(self, message, level, primary_metadata, secondary_metadata):
        with push_scope() as scope:
            scope.level = level
            for tag_name, tag_value in primary_metadata.items():
                scope.set_tag(tag_name, tag_value)
            for tag_name, tag_value in secondary_metadata.items():
                scope.set_extra(tag_name, tag_value)
            self._client.capture_message(message)
