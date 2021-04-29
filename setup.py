#! /usr/bin/env python
"""Installation script."""

from setuptools import setup

setup(
    name='jsonproto',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    author='Richard Neumann',
    author_email='mail@richard-neumann.de',
    python_requires='>=3.9',
    packages=['jsonproto'],
    scripts=['scripts/client', 'scripts/server'],
    url='https://github.com/conqp/jsonproto',
    license='GPLv3',
    description='A JSON-based client / server network protocol.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    keywords='JSON protocol network'
)
