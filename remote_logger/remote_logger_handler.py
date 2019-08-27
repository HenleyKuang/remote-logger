"""
:author: Henley Kuang
:since: 08/13/2019
"""

from logging import StreamHandler

from remote_logger.clients.sentry_logger_client import SentryLoggerClient
from remote_logger.clients.stackdriver_logger_client import StackdriverLoggerClient
from remote_logger.util.excepts import (
    InvalidClientTypeException,
)

CLIENT_TYPES = [SentryLoggerClient, StackdriverLoggerClient]


class RemoteLoggerHandler(StreamHandler):

    def __init__(self, client):
        StreamHandler.__init__(self)
        if type(client) not in CLIENT_TYPES:
            raise InvalidClientTypeException(
                "Invalid LoggerClient type (%s). Must be one of %s" % (
                    type(client), CLIENT_TYPES))
        self._client = client

    def emit(self, record):
        msg = self.format(record)
        level = record.levelname
        primary_metadata = {}
        secondary_metadata = {}
        group_id = None
        try:
            group_id = record.__dict__['group_id']
        except KeyError:
            pass
        try:
            primary_metadata = record.__dict__['primary_metadata']
        except KeyError:
            pass
        try:
            secondary_metadata = record.__dict__['secondary_metadata']
        except KeyError:
            pass
        self._client.send_log(msg,
                              level,
                              group_id,
                              primary_metadata,
                              secondary_metadata)
