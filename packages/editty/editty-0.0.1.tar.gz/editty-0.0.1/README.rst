Editty
======

Editty is a terminal-based non-linear editor for terminal recordings.

Installation
------------

Source
~~~~~~

When installing from source, it is recommended (but not required) to
install Editty in a virtualenv.  To set one up::

  virtualenv --python=python3 editty-env
  source editty-env/bin/activate

To install the latest version from pypi::

  pip install editty

To install from a git checkout::

  pip install .

In order to use the dissolve transition, you must run Editty in a
256-color capable terminal, such as gnome-terminal or xterm.

Usage
-----

After installing Editty, you should be able to run it by invoking
``editty``.  If you installed it in a virtualenv, you can invoke it
without activating the virtualenv with ``/path/to/editty-venv/bin/editty``.
which you may wish to add to your shell aliases.  Use ``editty
--help`` to see a list of command line options available.

Once running, pressing the F1 key will show help text.

Editty can load recordings in the formats produced by the ``script``
and ``ttyrec`` commands.  It renders output in ``ttyrec`` format.

Editty does not modify the original source files, but rather
references them by path name.  Editty stores the edit decision list in
its own JSON-based file format (use the ``.edit`` extension).

To exit, press CTRL-q.

Source
------

Git repo: http://git.inaugust.com/cgit/editty/

Contributing
------------

To send your latest commit as a patch, run::

  git send-email --to corvus@gnu.org --annotate -1

Or, if you don't have ``git send-email`` configured, run::

  git format-patch --stdout HEAD~1 > /tmp/editty.patch

And send `/tmp/editty.patch` to corvus@gnu.org using your email
client.

License
-------

Editty is licensed under the GPLv3 or later.  Please see the COPYING
file for details.
