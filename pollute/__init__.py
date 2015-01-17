import os
import sys
from contextlib2 import contextmanager
from functools import partial
from itertools import chain


#
# Public Interface
#

@contextmanager
def modified_environ(added=None, absent=()):
    """
    Temporarily updates the os.environ dictionary in-place. Can be used as a
    context manager or a decorator.

    The os.environ dictionary is updated in-place so that the modification is
    sure to work in all situations.

    :param added: Dictionary of environment variables and values to set.
    :param absent: List of environment variables to unset.
    """
    env = os.environ
    added = dict(added or {})
    absent = tuple(absent)

    in_env = partial(__filter, lambda i: i in env)
    not_in_env = partial(__filter, lambda i: i not in env)

    # List of environment variables being updated or removed.
    stomped = in_env(chain(__keys(added), absent))
    # Environment variables and values to restore on exit.
    update_after = dict((a, env[a]) for a in stomped)
    # Environment variables and values to remove on exit.
    remove_after = tuple(not_in_env(__keys(added)))

    def update(other):
        return env.update(other)

    def popper(item):
        return env.pop(item, None)

    def remove(items):
        return tuple(__map(popper, items))

    try:
        update(added)
        remove(absent)
        yield
    finally:
        update(update_after)
        remove(remove_after)


#
# Private Helpers
#

if sys.version_info >= (3, 0):
    __map = map                                 # pragma: no cover
    __filter = filter                           # pragma: no cover
    __keys = dict.keys                          # pragma: no cover
    __items = dict.items                        # pragma: no cover
else:                                           # pragma: no cover
    from itertools import imap as __map         # pragma: no cover
    from itertools import ifilter as __filter   # pragma: no cover
    __keys = dict.iterkeys                      # pragma: no cover
    __items = dict.iteritems                    # pragma: no cover
