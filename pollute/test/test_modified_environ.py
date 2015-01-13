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
    #        | var_a | var_b | var_c | var_d | var_e |
    # -------+---------------------------------------+
    # Before | val_a | val_b | val_c |       |       |
    # During | val_a | stomp |       | added |       |
    # After  | val_a | val_b | val_c |       | man_e |

    added = {
        'var_b': 'stomp',  # stomp an existing var
        'var_d': 'added'}  # add a new var

    absent = (
        'var_c',  # remove an existing var
        'var_e')  # remove a non-existent var

    expected_before = {
        'var_a': 'val_a',
        'var_b': 'val_b',
        'var_c': 'val_c'}

    expected_during = {
        'var_a': 'val_a',
        'var_b': 'stomp',
        'var_d': 'added'}

    expected_after = {
        'var_a': 'val_a',
        'var_b': 'val_b',
        'var_c': 'val_c',
        'var_e': 'man_e'}

    def before():
        os.environ.clear()
        os.environ.update(expected_before)
        eq_(dict(os.environ), expected_before)

    def during():
        eq_(dict(os.environ), expected_during)
        os.environ.update({
            'var_d': 'man_d',   # stomp an existing var
            'var_e': 'man_e'})  # add a new var

    def after():
        eq_(dict(os.environ), expected_after)

    test_scenarios = partial(
        __ensure_usage,
        kwargs=dict(
            added=added,
            absent=absent),
        before=before,
        during=during,
        after=after)

    for s in test_scenarios():
        yield s


#
# Test Helpers
#

def __ensure_usage(
        kwargs,
        before=lambda: None,
        during=lambda: None,
        after=lambda: None):
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
