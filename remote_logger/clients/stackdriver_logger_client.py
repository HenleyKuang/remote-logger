"""
:author: Henley Kuang
:since: 08/15/2019
"""
import logging
import google.cloud.logging

ERROR_REPORTING_TYPE = "type.googleapis.com/google.devtools.clouderrorreporting.v1beta1.ReportedErrorEvent"


class StackdriverLoggerClient(object):

    _error_reporting_level = logging.NOTSET

    def __init__(self, **kwargs):
        if 'service_key_path' in kwargs:
            credentials_path = kwargs['service_key_path']
            google_logging_client = google.cloud.logging.Client.from_service_account_json(
                credentials_path)
        else:
            google_logging_client = google.cloud.logging.Client()
        if 'error_reporting_level' in kwargs:
            self._error_reporting_level = kwargs['error_reporting_level']
            assert type(self._error_reporting_level) == int
        stackdriver_logger = google_logging_client.logger(__name__)
        self._client = stackdriver_logger

    def send_log(self, message, level, group_id, primary_metadata, secondary_metadata):
        # Merge primary and secondary metadata
        metadata_dict = {**primary_metadata, **secondary_metadata}
        metadata_dict['message'] = message
        if group_id is not None:
            metadata_dict["group_id"] = group_id
        if self._error_reporting_level != logging.NOTSET:
            metadata_dict['@type'] = ERROR_REPORTING_TYPE
        self._client.log_struct(metadata_dict, severity=level)
