"""
:author: Henley Kuang
:since: 08/13/2019
"""

from logging import StreamHandler

from remote_logger.clients.sentry_logger_client import SentryLoggerClient
from remote_logger.util.definitions import SENTRY


class RemoteLoggerHandler(StreamHandler):

    def __init__(self, client_type, **kwargs):
        StreamHandler.__init__(self)
        if client_type == SENTRY:
            self._client = SentryLoggerClient(**kwargs)

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
