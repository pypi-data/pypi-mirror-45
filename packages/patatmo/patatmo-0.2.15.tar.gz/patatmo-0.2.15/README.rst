patatmo Python package
======================

|build-badge| |docs-badge| |coverage-badge| |pypi-badge|

This package provides easy access to the `Netatmo <https://netatmo.com>`_
`API <https://dev.netatmo.com>`_.  It is **painless** as it completely and
intelligently hides the OAuth2 authentication from you.

Disclaimer
++++++++++

    **This software to access the** `Netatmo Weather API <https://dev.netatmo.com/>`_
    **emerged as part of thesis and also out of private interest.
    The author is not in any way affiliated with Netatmo (SAS).**

Capabilities
++++++++++++

Currently, the weather API's methods ``Getpublicdata``, ``Getstationsdata`` and
``Getmeasure`` are implemented.


Example usage
+++++++++++++

An example of obtaining all public station's data in the region of
Hamburg/Germany:

From the command-line
---------------------

The smart way is to set up a configuration file `~/.patatmo/settings.conf`:


.. code::

    [account]
    username=user.email@internet.com
    password=5uP3rP45sW0rD
    client_id=03012823b3fd2e420fbf980b
    client_secret=YXNkZmFzZGYgamFzamYgbGFzIG

Then on the command-line:

.. code:: sh

    netatmo-getpublicdata \
        --lat_ne 53.7499 \
        --lat_sw 53.3809 \
        --lon_ne 10.3471 \
        --lon_sw 9.7085

As one-liner:

.. code:: sh

    netatmo-getpublicdata \
        --user "user.email@internet.com" \
        --password "5uP3rP45sW0rD" \
        --id "5uP3rP45sW0rD" \
        --secret "YXNkZmFzZGYgamFzamYgbGFzIG" \
        --lat_ne 53.7499 \
        --lat_sw 53.3809 \
        --lon_ne 10.3471 \
        --lon_sw 9.7085

With environment variables (which you could also set elsewhere,
e.g. in your ``.bashrc``):

.. code:: sh

    export NETATMO_USERNAME="user.email@internet.com"
    export NETATMO_PASSWORD="5uP3rP45sW0rD"
    export NETATMO_CLIENT_ID="03012823b3fd2e420fbf980b"
    export NETATMO_CLIENT_SECRET="YXNkZmFzZGYgamFzamYgbGFzIG"
    netatmo-getpublicdata \
        --lat_ne 53.7499 \
        --lat_sw 53.3809 \
        --lon_ne 10.3471 \
        --lon_sw 9.7085


From Python
-----------

An example of obtaining all public station's data in the region of
Hamburg/Germany:

.. code:: python

    import patatmo

    # your netatmo connect developer credentials
    credentials = {
        "password":"5uP3rP45sW0rD",
        "username":"user.email@internet.com",
        "client_id":    "03012823b3fd2e420fbf980b",
        "client_secret":"YXNkZmFzZGYgamFzamYgbGFzIG"
    }

    # configure the authentication
    authentication = patatmo.api.authentication.Authentication(
        credentials=credentials,
        tmpfile = "temp_auth.json"
    )
    # providing a path to a tmpfile is optionally.
    # If you do so, the tokens are stored there for later reuse,
    # e.g. next time you invoke this script.
    # This saves time because no new tokens have to be requested.
    # New tokens are then only requested if the old ones expire.

    # create a api client
    client = patatmo.api.client.NetatmoClient(authentication)

    # lat/lon outline of Hamburg/Germany
    hamburg_region = {
        "lat_ne" : 53.7499,
        "lat_sw" : 53.3809,
        "lon_ne" : 10.3471,
        "lon_sw" : 9.7085,
    }

    # issue the API request
    hamburg = client.Getpublicdata(region = hamburg_region)

    # convert the response to a pandas.DataFrame
    print(hamburg.dataframe.to_csv())


.. code::

    ,index,altitude,humidity,id,latitude,longitude,pressure,temperature,time_humidity,time_pressure,time_temperature,timezone
    0,0,30.0,67.0,70:ee:50:12:9a:b8,53.51695,10.15599,1015.4,22.5,2017-08-26 16:36:19,2017-08-26 16:36:36,2017-08-26 16:36:19,Europe/Berlin
    1,1,23.0,65.0,70:ee:50:03:da:4c,53.523361337741,10.16719281615,1013.2,22.8,2017-08-26 16:35:33,2017-08-26 16:36:11,2017-08-26 16:35:33,Europe/Berlin
    2,2,25.0,80.0,70:ee:50:02:95:92,53.517903,10.165769,1016.9,21.5,2017-08-26 16:38:17,2017-08-26 16:38:23,2017-08-26 16:38:17,Europe/Berlin
    3,3,,,70:ee:50:17:bd:96,53.530789,10.127101,1010.1,,,2017-08-26 16:35:01,,Europe/Berlin
    4,4,15.0,83.0,70:ee:50:03:bc:2c,53.530948,10.134062,1013.5,20.6,2017-08-26 16:35:07,2017-08-26 16:35:25,2017-08-26 16:35:07,Europe/Berlin
    5,5,29.0,72.0,70:ee:50:03:72:28,53.545417580965,10.160120337925,1013.7,22.5,2017-08-26 16:42:05,2017-08-26 16:42:40,2017-08-26 16:42:05,Europe/Berlin
    6,6,24.0,70.0,70:ee:50:14:42:1c,53.5698669,10.1554532,1011.4,23.2,2017-08-26 16:33:11,2017-08-26 16:33:55,2017-08-26 16:33:11,Europe/Berlin
    7,7,31.0,69.0,70:ee:50:06:92:40,53.57426932987,10.161323698426,1013.7,22.3,2017-08-26 16:35:02,2017-08-26 16:35:30,2017-08-26 16:35:02,Europe/Berlin
    8,8,26.0,68.0,70:ee:50:01:3c:f6,53.5811,10.1485,1016.2,23.2,2017-08-26 16:40:57,2017-08-26 16:41:21,2017-08-26 16:40:57,Europe/Berlin


Install
+++++++

This package is on `PyPi <https://pypi.python.org/pypi/patatmo>`_. To install `patatmo`,
run

.. code:: sh

    pip install --user patatmo

Documentation
+++++++++++++

You can find detailed documentation of this package
`here on on Gitlab <https://nobodyinperson.gitlab.io/python3-patatmo/>`_.

Development
+++++++++++

The following might only be interesting for developers

Local installation
------------------

Install this module from the repository root via :code:`pip`:

.. code:: sh

    # local user library under ~/.local
    pip3 install --user .
    # in "editable" mode
    pip3 install --user -e .

Testing
-------

To be able to run *all* tests, you need to specify valid **credentials and a
device and model id** of your test station. You can do so either in the file
``tests/USER_DATA.json`` (e.g. copy the example file :code:`cp
tests/USER_DATA.json.example tests/USER_DATA.json` and adjust it) or via the
environment variables

.. code:: sh

    NETATMO_CLIENT_ID
    NETATMO_CLIENT_SECRET
    NETATMO_USERNAME
    NETATMO_PASSWORD
    NETATMO_DEVICE_ID
    NETATMO_MODULE_ID

Otherwise, only the possible tests are run.

Then:

- ``make test`` to run all tests directly
- ``make testverbose`` to run all tests directly with verbose output
- ``make setup-test`` to run all tests via the ``./setup.py test`` mechanism
- ``make coverage`` to get a test coverage

Versioning
----------

- ``make increase-patch`` to increase the patch version number
- ``make increase-minor`` to increase the minor version number
- ``make increase-major`` to increase the major version number


.. |build-badge| image:: https://gitlab.com/nobodyinperson/python3-patatmo/badges/master/build.svg
    :target: https://gitlab.com/nobodyinperson/python3-patatmo/commits/master
    :alt: Build

.. |docs-badge| image:: https://img.shields.io/badge/docs-sphinx-brightgreen.svg
    :target: https://nobodyinperson.gitlab.io/python3-patatmo/
    :alt: Documentation

.. |coverage-badge| image:: https://gitlab.com/nobodyinperson/python3-patatmo/badges/master/coverage.svg
    :target: https://nobodyinperson.gitlab.io/python3-patatmo/coverage-report
    :alt: Coverage

.. |pypi-badge| image:: https://badge.fury.io/py/patatmo.svg
   :target: https://badge.fury.io/py/patatmo
   :alt: PyPi

