from setuptools import setup

setup(
    name='pollute',
    version='1.0.1',
    packages=('pollute',),
    url='https://github.com/themattrix/python-pollute',
    license='MIT',
    author='Matthew Tardiff',
    author_email='mattrix@gmail.com',
    install_requires=('contextlib2',),
    tests_require=('nose',),
    description=(
        'A decorator and context manager for temporarily modifying '
        'os.environ.'),
    classifiers=(
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'))
