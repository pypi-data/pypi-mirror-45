=====
pyAS2
=====

.. image:: https://img.shields.io/pypi/v/pyAS2.svg
    :target: https://pypi.python.org/pypi/pyAS2

.. image:: https://readthedocs.org/projects/pyas2/badge/?version=latest 
    :target: http://pyas2.readthedocs.org
    :alt: Latest Docs


``pyAS2`` is an AS2 server/client written in python and built on the django framework.
The application supports AS2 version 1.2 as defined in the `RFC 4130`_. Our goal is to provide a native
python library for implementing the AS2 protocol. It supports Python 2.6-2.7.

``pyAS2`` includes a set of django-admin commands that can be used to start the server, send files as
a client, send asynchronous MDNs and so on. It also has a web based front end interface for
configuring partners and organizations, monitoring message transfers and also initiating new transfers.

Features
~~~~~~~~

* Technical

    * Asyncronous and syncronous MDN
    * Partner and Organization management
    * Digital signatures
    * Message encryption
    * Secure transport (SSL)
    * Support for SSL client authentication
    * System task to auto clear old log entries
    * Data compression (AS2 1.1)
    * Multinational support: Uses Django's internationalization feature

* Integration

    * Easy integration to existing systems, using a partner based file system interface
    * Daemon Process picks up data from directories when it becomes available
    * Message post processing (scripting on receipt)

* Monitoring

    * Web interface for transaction monitoring
    * Email event notification

* The following encryption algorithms are supported:

    * Triple DES
    * DES
    * RC2-40
    * AES-128
    * AES-192
    * AES-256

* The following hash algorithms are supported:

    * SHA-1

Documentation
~~~~~~~~~~~~~

You can find more information in the `documentation`_.

Discussion
~~~~~~~~~~

If you run into bugs, you can file them in our `issue tracker`_.

Contribute
~~~~~~~~~~

#. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
#. Fork `the repository`_ on GitHub to start making your changes to the **master** branch (or branch off of it).
#. Create your feature branch: `git checkout -b my-new-feature`
#. Commit your changes: `git commit -am 'Add some feature'`
#. Push to the branch: `git push origin my-new-feature`
#. Send a pull request and bug the maintainer until it gets merged and published. :) Make sure to add yourself to AUTHORS_.

Running Tests
~~~~~~~~~~~~~

To run ``pyAS2's`` test suite:

``django-admin.py test pyas2 --settings=pyas2.test_settings --pythonpath=.``

License
~~~~~~~

GNU GENERAL PUBLIC LICENSE
                       Version 2, June 1991

 Copyright (C) 1989, 1991 Free Software Foundation, Inc., <http://fsf.org/>
 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

.. _`RFC 4130`: https://www.ietf.org/rfc/rfc4130.txt
.. _`documentation`: http://pyas2.readthedocs.org
.. _`the repository`: http://github.com/abhishek-ram/pyas2
.. _AUTHORS: https://github.com/abhishek-ram/pyas2/blob/master/AUTHORS.rst
.. _`issue tracker`: https://github.com/abhishek-ram/pyas2/issues
