import argparse
import logging

from remote_logger.clients.sentry_logger_client import SentryLoggerClient
from remote_logger.clients.stackdriver_logger_client import StackdriverLoggerClient
from remote_logger.remote_logger_handler import RemoteLoggerHandler

LOGGER = logging.getLogger(__name__)


def _parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)

    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('--level',
                               action='store',
                               choices=['debug', 'info',
                                        'warning', 'error',
                                        'critical'],
                               default='info',
                               help='log level')

    sentry_parser = argparse.ArgumentParser(add_help=False)
    sentry_parser.add_argument('--dsn',
                               action='store',
                               required=True,
                               help='dsn endpoint')

    stackdriver_parser = argparse.ArgumentParser(add_help=False)
    stackdriver_parser.add_argument('--service-key-path',
                                    action='store',
                                    help='service key json path')
    stackdriver_parser.add_argument('--error-reporting-level',
                                    action='store',
                                    choices=['debug', 'info',
                                             'warning', 'error',
                                             'critical'],
                                    default='error',
                                    help='log level to send events to error reporting')

    command_subparser = parser.add_subparsers(dest='client_type')
    command_subparser.required = True
    command_subparser.add_parser("sentry", parents=[parent_parser,
                                                    sentry_parser])
    command_subparser.add_parser("stackdriver", parents=[parent_parser,
                                                         stackdriver_parser])

    return parser.parse_args()


def _main():
    options = _parse_args()
    client_type = options.client_type
    level = options.level

    levelint = logging.getLevelName(level.upper())
    dummy_group_id = 99
    primary_metadata = {
        "pkey1": "pvalue1",
        "pkey2": "pvalue2",
        "pkey3": "pvalue3",
    }
    secondary_metadata = {
        "skey1": "svalue1",
        "skey2": "svalue2",
        "skey3": "svalue3",
    }

    client = None
    if client_type == "sentry":
        dsn = options.dsn
        client = SentryLoggerClient(dsn=dsn)
    elif client_type == "stackdriver":
        service_key_path = options.service_key_path
        error_reporting_level = options.error_reporting_level
        kwargs = {}
        if service_key_path is not None:
            kwargs['service_key_path'] = service_key_path
        if error_reporting_level is not None:
            error_reporting_levelint = logging.getLevelName(
                error_reporting_level.upper())
            kwargs['error_reporting_level'] = error_reporting_levelint
        client = StackdriverLoggerClient(**kwargs)
    remote_logger_handler = RemoteLoggerHandler(client)
    remote_logger_handler.setLevel(levelint)
    LOGGER.addHandler(remote_logger_handler)
    getattr(LOGGER, level)(msg="Test Message\n",
                           extra={
                               "group_id": dummy_group_id,
                               "primary_metadata": primary_metadata,
                               "secondary_metadata": secondary_metadata,
                           })


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    _main()
