"""
:author: Henley Kuang
:since: 08/15/2019
"""
from google.cloud import logging


class StackdriverLoggerClient(object):

    def __init__(self, **kwargs):
        if 'service_key_path' in kwargs:
            credentials_path = kwargs['service_key_path']
            google_logging_client = logging.Client.from_service_account_json(
                credentials_path)
        else:
            google_logging_client = logging.Client(**kwargs)
        stackdriver_logger = google_logging_client.logger(__name__)
        self._client = stackdriver_logger

    def send_log(self, message, level, group_id, primary_metadata, secondary_metadata):
        # Merge primary and secondary metadata
        metadata_dict = {**primary_metadata, **secondary_metadata}
        metadata_dict['message'] = message
        if group_id is not None:
            metadata_dict["group_id"] = group_id
        self._client.log_struct(metadata_dict, severity=level)
