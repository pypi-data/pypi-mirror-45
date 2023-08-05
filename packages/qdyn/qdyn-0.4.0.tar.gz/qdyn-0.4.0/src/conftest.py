"""Set up the environment for doctests

This file is automatically evaluated by py.test. It ensures that we can write
doctests without distracting import statements in the doctest.
"""
import numpy

# noinspection PyPackageRequirements
import pytest


@pytest.fixture(autouse=True)
def set_doctest_env(doctest_namespace):
    """Inject objects into the testing namespace"""
    doctest_namespace['numpy'] = numpy
