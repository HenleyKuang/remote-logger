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
    command_subparser.add_parser(SENTRY, parents=[sentry_parser])
    command_subparser.add_parser(STACKDRIVER)

    return parser.parse_args()


def _main():
    options = _parse_args()
    client_type = options.client_type
    dummy_group_id = 99
    primary_metadata = {
        "xpfdafkey1": "pvaldafasue1",
        "pkdafasey2": "pvfdasfasalue2",
        "pkdasfasey3": "pvaludafase3",
    }
    secondary_metadata = {
        "skdafasey1": "svadasfaslue1",
        "skey2": "svadasfaslue2",
        "skdasfasey3": "svdsfasalue3",
    }

    if client_type == SENTRY:
        dsn = options.dsn
        sentry_handler = RemoteLoggerHandler(client_type,
                                             dsn=dsn)
        sentry_handler.setLevel(logging.ERROR)
        LOGGER.addHandler(sentry_handler)
    elif client_type == STACKDRIVER:
        stackdriver_handler = RemoteLoggerHandler(client_type)
        stackdriver_handler.setLevel(logging.ERROR)
        LOGGER.addHandler(stackdriver_handler)
    LOGGER.error("T32423523est 54353", extra={
        "group_id": dummy_group_id,
        "primary_metadata": primary_metadata,
        "secondary_metadata": secondary_metadata,
    })


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    _main()
