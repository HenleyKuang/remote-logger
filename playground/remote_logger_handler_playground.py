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

    sentry_parser = argparse.ArgumentParser(add_help=False)
    sentry_parser.add_argument('--dsn',
                               action='store',
                               default='parent',
                               help='dsn endpoint')

    command_subparser = parser.add_subparsers(dest='client_type')
    command_subparser.required = True
    command_subparser.add_parser('sentry', parents=[sentry_parser])

    return parser.parse_args()


def _main():
    options = _parse_args()
    client_type = options.client_type

    if client_type == SENTRY:
        dsn = options.dsn
        dummy_group_id = None  # None = do not group
        sentry_handler = RemoteLoggerHandler(client_type,
                                             dsn=dsn)
        sentry_handler.setLevel(logging.ERROR)
        LOGGER.addHandler(sentry_handler)
        LOGGER.error("Test Message", extra={
            "group_id": dummy_group_id,
            "primary_metadata": {
                "pkey1": "pvalue1",
                "pkey2": "pvalue2",
                "pkey3": "pvalue3",
            },
            "secondary_metadata": {
                "skey1": "svalue1",
                "skey2": "svalue2",
                "skey3": "svalue3",
            }
        })


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    _main()
