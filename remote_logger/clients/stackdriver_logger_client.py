"""
:author: Henley Kuang
:since: 08/15/2019
"""
from google.cloud import logging


class StackdriverLoggerClient(object):

    def __init__(self, **kwargs):
        google_logging_client = logging.Client()
        stackdriver_logger = google_logging_client.logger(__name__)
        self._client = stackdriver_logger

    def send_log(self, message, level, group_id, primary_metadata, secondary_metadata):
        # Merge primary and secondary metadata
        # To filter by specific metadata, create labels
        #   (https://cloud.google.com/logging/docs/logs-based-metrics/labels)
        metadata_dict = {**primary_metadata, **secondary_metadata}
        metadata_dict['message'] = message
        if group_id is not None:
            metadata_dict["group_id"] = group_id
        self._client.log_struct(metadata_dict, severity=level)
