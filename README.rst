.. image:: https://img.shields.io/badge/License-GPL%20v3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0

.. image:: https://badge.fury.io/py/remote-logger.svg
   :target: https://pypi.org/project/remote-logger/

.. image:: https://img.shields.io/travis/HenleyKuang/remote-logger.svg
   :target: https://travis-ci.org/HenleyKuang/remote-logger

Remote Logger
=============

Installation
------------

.. code-block:: bash

    pip install remote-logger


Examples
--------

Initializing RemoteLogger with Sentry

.. code-block:: python

    import logging

    from remote_logger.remote_logger_handler import RemoteLoggerHandler
    from remote_logger.util.definitions import SENTRY

    LOGGER = logging.getLogger(__name__)

    client_type = SENTRY
    dsn = "https://<key>@sentry.io/<project>"
    sentry_handler = RemoteLoggerHandler(client_type,
                                         dsn=dsn)
    sentry_handler.setLevel(logging.ERROR)
    LOGGER.addHandler(sentry_handler)


Initializing RemoteLogger with Stackdriver

.. code-block:: python

    import logging

    from remote_logger.remote_logger_handler import RemoteLoggerHandler
    from remote_logger.util.definitions import STACKDRIVER

    LOGGER = logging.getLogger(__name__)

    client_type = STACKDRIVER

    # With service key
    service_key_path = "/path/to/key.json"
    stackdriver_handler = RemoteLoggerHandler(client_type,
                                              service_key_path=service_key_path)
    # Without service key
    stackdriver_handler = RemoteLoggerHandler(client_type)

    stackdriver_handler.setLevel(logging.ERROR)
    LOGGER.addHandler(stackdriver_handler)


Sending events to RemoteLogger

.. code-block:: python

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
    LOGGER.error("Test Message", extra={
        "group_id": dummy_group_id,
        "primary_metadata": primary_metadata,
        "secondary_metadata": secondary_metadata,
    })
