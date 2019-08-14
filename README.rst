Remote Logger
=============

Installation
------------

.. code-block:: bash

    pip install remote-logger


Examples
--------

Sentry

Code
    .. code-block:: python

        client_type = "sentry"
        dsn = https://<key>@sentry.io/<project>
        sentry_handler = RemoteLoggerHandler(client_type,
                                            dsn=dsn)
        sentry_handler.setLevel(logging.ERROR)
        LOGGER.addHandler(sentry_handler)
        LOGGER.error("Test Message", extra={
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

Result
    .. image:: https://raw.githubusercontent.com/HenleyKuang/remote-logger/master/img/SentryLogTestMessage.PNG
        :scale: 30%
