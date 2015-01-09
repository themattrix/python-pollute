import os
from pollute import modified_environ
from nose.tools import with_setup, eq_


#
# Setup and Teardown
#

__old_env = os.environ.copy()


def restore_environ():
    os.environ.clear()
    os.environ.update(__old_env)


#
# Tests
#

@with_setup(teardown=restore_environ)
def test_context_manager():
    __ensure_before()
    with modified_environ(**__updates):
        __ensure_during()
    __ensure_after()


@with_setup(teardown=restore_environ)
def test_decorator():
    @modified_environ(**__updates)
    def __update():
        __ensure_during()

    __ensure_before()
    __update()
    __ensure_after()


#
# Test Helpers
#

__updates = dict(
    added={'added_var': 'baz'},
    absent=('existing_var',))


def __ensure_before():
    eq_(dict(os.environ), __old_env)
    os.environ['existing_var'] = 'bar'


def __ensure_during():
    expected_env = {'added_var': 'baz'}
    expected_env.update(__old_env)
    eq_(dict(os.environ), expected_env)
    os.environ['manually_added_var'] = 'foo'


def __ensure_after():
    expected_env = {'manually_added_var': 'foo', 'existing_var': 'bar'}
    expected_env.update(__old_env)
    eq_(dict(os.environ), expected_env)
