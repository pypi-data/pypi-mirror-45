torrent_rename
==================

command line and module for rename torrent to original name


Installing
----------

Install and update using `pip`_:

.. code-block:: text

    $ pip install torrent_rename

torrent_rename supports Python 2 and newer, Python 3 and newer, and PyPy.

.. _pip: https://pip.pypa.io/en/stable/quickstart/


Example
----------------

What does it look like? Here is an example of a simple torrent_rename program:

.. code-block:: python

    from torrent_rename import torrent_rename

    tr = torrent_rename()
    
    torrent_file_path = r"/home/cumulus13/Download/74BC02344EC863D4CD9D5F942C1A0C3AE513746D.torrent"

    tr.rename(torrent_file_path, overwrite=True) #overwrite: True or auto (str), auto: auto rename torrent file


And what it looks like when run:

.. code-block:: text

    $ python test.py 
    FILE  :l:\temp\TORRENT_FILES\Jet Red.torrent
    NAME  : [('name7:', 'Jet Red', '12:')]
    NAME  : Jet Red
    RENAME: [OVERWRITE] Jet Red.torrent
    ---------------------------------------------------------------------------------------------------------------

You can run as command line

.. code-block:: batch

    $ torrent_rename "/home/cumulus13/Download/74BC02344EC863D4CD9D5F942C1A0C3AE513746D.torrent""
       FILE  :l:\temp\TORRENT_FILES\Jet Red.torrent
       NAME  : [('name7:', 'Jet Red', '12:')]
       NAME  : Jet Red
       RENAME: [OVERWRITE] Jet Red.torrent
       ---------------------------------------------------------------------------------------------------------------

Support
------

*   Python 2.7 +, Python 3.x
*   Windows, Linux

Links
-----

*   License: `BSD <https://github.com/licface/torrent_rename/src/default/LICENSE.rst>`_
*   Code: https://github.com/licface/torrent_rename
*   Issue tracker: https://github.com/licface/torrent_rename/issues