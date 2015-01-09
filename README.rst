Pollute |Version| |Build| |Coverage| |Health|
=============================================

|Compatibility| |Implementations| |Format| |Downloads|

A decorator and context manager for temporarily modifying ``os.environ``.

.. code:: python

    # as a context manager
    with modified_environ(added={...}, absent=[...]):
        ...

    # as a decorator
    @modified_environ(added={...}, absent=[...])


Installation:

.. code:: shell

    $ pip install pollute


``modified_environ`` modifies ``os.environ`` in-place, ensuring that all
references to it in the code are updated. All changes made by
``modified_environ`` are reversed when exiting the context or decorator.


Example
-------

.. code:: python

    import os
    from pollute import modified_environ


    assert 'HELLO' not in os.environ
    assert 'PATH' in os.environ

    with modified_environ(added={'HELLO': 'WORLD'}, absent=['PATH']):
        assert os.environ['HELLO'] == 'WORLD'
        assert 'PATH' not in os.environ

    assert 'HELLO' not in os.environ
    assert 'PATH' in os.environ


.. |Build| image:: https://travis-ci.org/themattrix/python-pollute.svg?branch=master
   :target: https://travis-ci.org/themattrix/python-pollute
.. |Coverage| image:: https://img.shields.io/coveralls/themattrix/python-pollute.svg
   :target: https://coveralls.io/r/themattrix/python-pollute
.. |Health| image:: https://landscape.io/github/themattrix/python-pollute/master/landscape.svg
   :target: https://landscape.io/github/themattrix/python-pollute/master
.. |Version| image:: https://pypip.in/version/pollute/badge.svg?text=version
    :target: https://pypi.python.org/pypi/pollute
.. |Downloads| image:: https://pypip.in/download/pollute/badge.svg
    :target: https://pypi.python.org/pypi/pollute
.. |Compatibility| image:: https://pypip.in/py_versions/pollute/badge.svg
    :target: https://pypi.python.org/pypi/pollute
.. |Implementations| image:: https://pypip.in/implementation/pollute/badge.svg
    :target: https://pypi.python.org/pypi/pollute
.. |Format| image:: https://pypip.in/format/pollute/badge.svg
    :target: https://pypi.python.org/pypi/pollute
