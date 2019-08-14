"""
:author: Henley Kuang
:since: 08/05/2019
"""


class LoggerClient(object):
    __slots__ = ('_client')

    def send_log(self, message, level, group_id, primary_metadata, secondary_metadata):
        """
        Report/Send a message to the server

        :param message: Message to send
        :type message: str
        :param level: Python Level Number - Severity of the event.
            (https://docs.python.org/3/library/logging.html#logging-levels)
        :type level: int
        :param group_id: Id to indicate how events should be grouped
        :type group_id: int
        :param primary_metadata: Payload of primary data to include with message
        :type primary_metadata: dict
        :param secondary_metadata: Payload of secondary data to include with message
        :type secondary_metadata: dict
        """
        raise NotImplementedError
