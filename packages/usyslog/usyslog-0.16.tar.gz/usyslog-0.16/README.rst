usyslog
==================

Simple remote syslog sender 


Installing
------------

Install and update using `pip`_:

.. code-block:: text

    $ pip install usyslog

usyslog supports Python 2 and newer, Python 3 and newer, and PyPy.

.. _pip: https://pip.pypa.io/en/stable/quickstart/


A Simple Example
-----------------

What does it look like? Here is an example of a simple usyslog program:

.. code-block:: python

    from usyslog import syslog

    message = "This is an error"
    
    syslog(message, level=LEVEL['error'], facility=FACILITY['daemon'],
	host='localhost', port=514)
	# default host = 'localhost'
	# default port = 514
	# or
	
	syslog(message, 3, 3, '192.168.0.1')


Support
--------

*   Python 2.7 +, Python 3.x
*   Windows, Linux

Links
-------

*   License: `BSD <https://bitbucket.org/licface/usyslog/src/LICENSE.rst>`_
*   Code: https://bitbucket.org/licface/usyslog
*   Issue tracker: https://bitbucket.org/licface/make_color/issues