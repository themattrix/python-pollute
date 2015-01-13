import os
from nose.tools import with_setup


#
# Setup/Teardown
#

__old_env = os.environ.copy()


def restore_env():
    os.environ.clear()
    os.environ.update(__old_env)


#
# Tests
#

@with_setup(teardown=restore_env)
def test_example_1():
    from pollute.test.example_1 import example
    assert example
