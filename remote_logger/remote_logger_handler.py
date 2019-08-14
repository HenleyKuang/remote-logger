"""
:author: Henley Kuang
:since: 08/13/2019
"""

from logging import StreamHandler

from remote_logger.clients.sentry_logger_client import SentryLoggerClient
from remote_logger.util.definitions import SENTRY
from remote_logger.util.excepts import InvalidClientTypeException

CLIENT_TYPE_LOGGER_CLIENT = {
    SENTRY: SentryLoggerClient,
}


class RemoteLoggerHandler(StreamHandler):

    def __init__(self, client_type, **kwargs):
        StreamHandler.__init__(self)
        try:
            LoggerClient = CLIENT_TYPE_LOGGER_CLIENT[client_type]
        except KeyError:
            raise InvalidClientTypeException(
                "No LoggerClient for client_type: %s" % client_type)
        self._client = LoggerClient(**kwargs)

    def emit(self, record):
        msg = self.format(record)
        level = record.levelname
        primary_metadata = {}
        secondary_metadata = {}
        try:
            primary_metadata = record.__dict__['primary_metadata']
        except Exception:
            pass
        try:
            secondary_metadata = record.__dict__['secondary_metadata']
        except Exception:
            pass
        self._client.send_log(msg, level, primary_metadata, secondary_metadata)
