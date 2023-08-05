Developing
==========

The `Cutadapt source code is on GitHub <https://github.com/marcelm/cutadapt/>`_.
Cutadapt is written in Python 3 with some extension modules that are written
in Cython. Support for Python 2 has been dropped.


Development installation
------------------------

For development, make sure that you install Cython and tox. We also recommend
using a virtualenv. This sequence of commands should work::

    git clone https://github.com/marcelm/cutadapt.git  # or clone your own fork
    cd cutadapt
    python3 -m venv venv
    venv/bin/pip3 install Cython pytest nose tox
    venv/bin/pip3 install -e .

Then you can run Cutadapt like this (or activate the virtualenv and omit the
``venv/bin`` part)::

    venv/bin/cutadapt --help

The tests can then be run like this::

    venv/bin/pytest

Or with tox (but then you will need to have binaries for all tested Python
versions installed)::

    venv/bin/tox


Development installation (without virtualenv)
---------------------------------------------

Alternatively, if you do not want to use virtualenv, running the following may
work from within the cloned repository::

    python3 setup.py build_ext -i
    pytest

This requires Cython and pytest to be installed. Avoid this method and use a
virtualenv instead if you can.


Code style
----------

Cutadapt tries to follow PEP8, with some exceptions:

* Indentation is made with tabs, not with spaces
* The maximum line length for code 100 characters, not 80, but try to wrap
  comments at 80 characters for readability.

Yes, there are inconsistencies in the current code base since it’s a few years old already.


Making a release
----------------

Since version 1.17, Travis CI is used to automatically deploy a new Cutadapt release
(both as an sdist and as wheels) whenever a new tag is pushed to the Git repository.

Cutadapt uses `versioneer <https://github.com/warner/python-versioneer>`_ to automatically manage
version numbers. This means that the version is not stored in the source code but derived from
the most recent Git tag. The following procedure can be used to bump the version and make a new
release.

#. Update ``CHANGES.rst`` (version number and list of changes)

#. Ensure you have no uncommitted changes in the working copy.

#. Run a ``git pull``.

#. Run ``tox``, ensuring all tests pass.

#. Tag the current commit with the version number (there must be a ``v`` prefix)::

       git tag v0.1

   To release a development version, use a ``dev`` version number such as ``v1.17.dev1``.
   Users will not automatically get these unless they use ``pip install --pre``.

#. Push the tag::

       git push --tags

#. Wait for Travis to finish and to deploy to PyPI.

#. Update the `bioconda recipe <https://github.com/bioconda/bioconda-recipes/blob/master/recipes/cutadapt/meta.yaml>`_.
   It is probly easiest to edit the recipe via the web interface and send in a
   pull request. Ensure that the list of dependencies (the ``requirements:``
   section in the recipe) is in sync with the ``setup.py`` file.

   Since this is just a version bump, the pull request does not need a
   review by other bioconda developers. As soon as the tests pass and if you
   have the proper permissions, it can be merged directly.


Releases to bioconda still need to be made manually.


Making a release manually
-------------------------

.. note:
    This section is outdated, see the previous section!

If this is the first time you attempt to upload a distribution to PyPI, create a
configuration file named ``.pypirc`` in your home directory with the following
contents::

    [distutils]
    index-servers =
        pypi

    [pypi]
    username=my-user-name
    password=my-password

See also `this blog post about getting started with
PyPI <http://peterdowns.com/posts/first-time-with-pypi.html>`_. In particular,
note that a ``%`` in your password needs to be doubled and that the password
must *not* be put between quotation marks even if it contains spaces.

Cutadapt uses `versioneer <https://github.com/warner/python-versioneer>`_ to automatically manage
version numbers. This means that the version is not stored in the source code but derived from
the most recent Git tag. The following procedure can be used to bump the version and make a new
release.

#. Update ``CHANGES.rst`` (version number and list of changes)

#. Ensure you have no uncommitted changes in the working copy.

#. Run a ``git pull``.

#. Run ``tox``, ensuring all tests pass.

#. Tag the current commit with the version number (there must be a ``v`` prefix)::

       git tag v0.1

#. Create a distribution (``.tar.gz`` file). Double-check that the auto-generated version number in
   the tarball is as you expect it by looking at the name of the generated file in ``dist/``::

       python3 setup.py sdist

#. If necessary, pip install ``twine`` and then upload the generated tar file to PyPI::

       twine upload dist/cutadapt-0.1.tar.gz  # adjust version number

#. Push the tag::

       git push --tags

#. Update the `bioconda recipe <https://github.com/bioconda/bioconda-recipes/blob/master/recipes/cutadapt/meta.yaml>`_.
   It is probly easiest to edit the recipe via the web interface and send in a
   pull request. Ensure that the list of dependencies (the ``requirements:``
   section in the recipe) is in sync with the ``setup.py`` file.

   Since this is just a version bump, the pull request does not need a
   review by other bioconda developers. As soon as the tests pass and if you
   have the proper permissions, it can be merged directly.

If something went wrong *after* you uploaded a tarball, fix the problem and follow the
above instructions again, but with an incremented revision in the version number.
That is, go from version x.y to x.y.1. Do not change a version that has already
been uploaded.
