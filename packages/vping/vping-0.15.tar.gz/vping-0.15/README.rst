vping
==================

PING module


Installing
----------

Install and update using `pip`_:

.. code-block:: text

    $ pip install vping

vping supports Python 2 and newer, Python 3 and newer, and PyPy.

.. _pip: https://pip.pypa.io/en/stable/quickstart/


Example
----------------

What does it look like? Here is an example of a simple vping program:

.. code-block:: python

    import vping
    host = "www.google.com"
    timeout = 10 #default: 2
    count = 5 #default=4
    
    vping.verbose_ping(host, timeout, count)


And what it looks like when run:

.. code-block:: text

    $ python test.py 
      ping www.google.com...
      get ping in 10.9999 milliseconds.
      ping www.google.com...
      get ping in 0.0 milliseconds.
      ping www.google.com...
      get ping in 0.0 milliseconds.
      ping www.google.com...
      get ping in 0.0 milliseconds.

You can just run vping on terminal

.. code-block:: batch

    $ vping.py www.google.com
      ping www.google.com...
      get ping in 10.9999 milliseconds.
      ping www.google.com...
      get ping in 0.0 milliseconds.
      ping www.google.com...
      get ping in 0.0 milliseconds.
      ping www.google.com...
      get ping in 0.0 milliseconds.


Support
------

*   Python 2.7 +, Python 3.x
*   Windows, Linux

Links
-----

*   License: `BSD <https://bitbucket.org/licface/vping/src/default/LICENSE.rst>`_
*   Code: https://bitbucket.org/licface/vping
*   Issue tracker: https://bitbucket.org/licface/vping/issues