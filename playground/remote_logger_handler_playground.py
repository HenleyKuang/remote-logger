import argparse
import logging

from remote_logger.remote_logger_handler import RemoteLoggerHandler
from remote_logger.util.definitions import (
    SENTRY,
    STACKDRIVER,
)

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

    command_subparser = parser.add_subparsers(dest='client_type')
    command_subparser.required = True
    command_subparser.add_parser(SENTRY, parents=[parent_parser,
                                                  sentry_parser])
    command_subparser.add_parser(STACKDRIVER, parents=[parent_parser,
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

    if client_type == SENTRY:
        dsn = options.dsn
        sentry_handler = RemoteLoggerHandler(client_type,
                                             dsn=dsn)
        sentry_handler.setLevel(levelint)
        LOGGER.addHandler(sentry_handler)
    elif client_type == STACKDRIVER:
        service_key_path = options.service_key_path
        if service_key_path is not None:
            stackdriver_handler = RemoteLoggerHandler(client_type,
                                                      service_key_path=service_key_path)
        else:
            stackdriver_handler = RemoteLoggerHandler(client_type)
        stackdriver_handler.setLevel(levelint)
        LOGGER.addHandler(stackdriver_handler)
    getattr(LOGGER, level)(msg="Test Message",
                           extra={
                               "group_id": dummy_group_id,
                               "primary_metadata": primary_metadata,
                               "secondary_metadata": secondary_metadata,
                           })


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    _main()
