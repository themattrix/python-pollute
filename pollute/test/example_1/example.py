import os
from pollute import modified_environ


assert 'HELLO' not in os.environ
assert 'PATH' in os.environ

with modified_environ(added={'HELLO': 'WORLD'}, absent=['PATH']):
    assert os.environ['HELLO'] == 'WORLD'
    assert 'PATH' not in os.environ

assert 'HELLO' not in os.environ
assert 'PATH' in os.environ
