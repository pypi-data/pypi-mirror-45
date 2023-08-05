eam
===

A package providing management entry points allowing a bundle to be
used as an application.


Setup
=====

Create the development environment with the desired python version::

  edm envs create eam-dev --version=2
  edm install -e eam-dev haas enum34 -y
  edm run -e eam-dev -- pip install -e .
  edm run -e eam-dev -- pip install -e eam_example_app/

.. note::

   - Similarly a normal python or virtualenv environment can be used.
   - On Windows platforms one needs to also install ``comtypes``
   - ``enum34`` is only needed for python 2.7

Test
====

Run the tests in the development environment::

  edm run -e eam-dev -- haas -v eam


Using the ci console tool
=========================

The ci helper package in the source repository aids in setting up a
development environment and running tests. It requires
EDM, along with a Python bootstrap environment equipped with click.

To create a development environment, run::

  python -m ci build

from the top-level of the repository, within the Python bootstrap environment.

To run tests for the eam EDM environment, do::

  python -m ci test

To run tests under coverage::

  python -m ci coverage

To run a style check::

  python -m ci flake8
