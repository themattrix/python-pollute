import os
from functools import partial
from nose.tools import with_setup, eq_
from pollute import modified_environ


#
# Tests
#

def test_no_changes():
    old_env = os.environ.copy()

    def ensure_no_changes():
        eq_(dict(os.environ), old_env)

    test_scenarios = partial(
        __ensure_usage,
        kwargs={},
        before=ensure_no_changes,
        during=ensure_no_changes,
        after=ensure_no_changes)

    for s in test_scenarios():
        yield s


def test_happy_path():
    old_env = os.environ.copy()

    added = {
        'added_var_a': 'added_a',
        'added_var_b': 'added_b'}

    absent = (
        'existing_var_a',
        'existing_var_b')

    def ensure_before():
        eq_(dict(os.environ), old_env)
        os.environ['existing_var_a'] = 'existing_a'
        os.environ['existing_var_b'] = 'existing_b'

    def ensure_during():
        expected_env = added.copy()
        expected_env.update(old_env)
        eq_(dict(os.environ), expected_env)
        os.environ['manually_added_var_a'] = 'manual_a'
        os.environ['manually_added_var_b'] = 'manual_b'

    def ensure_after():
        expected_env = {
            'manually_added_var_a': 'manual_a',
            'manually_added_var_b': 'manual_b',
            'existing_var_a': 'existing_a',
            'existing_var_b': 'existing_b'}
        expected_env.update(old_env)
        eq_(dict(os.environ), expected_env)

    test_scenarios = partial(
        __ensure_usage,
        kwargs=dict(
            added=added,
            absent=absent),
        before=ensure_before,
        during=ensure_during,
        after=ensure_after)

    for s in test_scenarios():
        yield s


#
# Test Helpers
#

def __ensure_usage(kwargs, before, during, after):
    old_env = os.environ.copy()

    def restore_environ():
        os.environ.clear()
        os.environ.update(old_env)

    @with_setup(teardown=restore_environ)
    def ensure_context_manager():
        before()
        with modified_environ(**kwargs):
            during()
        after()

    @with_setup(teardown=restore_environ)
    def ensure_decorator():
        @modified_environ(**kwargs)
        def inner():
            during()

        before()
        inner()
        after()

    yield ensure_context_manager
    yield ensure_decorator
