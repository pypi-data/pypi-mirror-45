"""
Project: Page Rank
Tue Apr 12 16:33:53 2019
"""

import os
import re

from setuptools import setup, find_packages

try: # for pip >= 10
    from pip._internal.req import parse_requirements
    from pip._internal.download import PipSession
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements
    from pip.download import PipSession

# Author
__author__ = 'Jason Xing Zhang'
__email__ = 'jason.xing.zhang@gmail.com'


def read_requirements_file(path):
    """
    reads requirements.txt file and handles PyPI index URLs

    Args:
        path (str): path to requirements.txt file

    Returns:
        (tuple of lists)
    """
    session = PipSession()
    base_path = os.path.dirname(path)

    # cache dependencies between files
    _cached_links = {}

    def find_extra_url(filename):
        """
        get the --extra-find_extra_url from the file

        Args:
            filename (str): file name

        Returns:
            find_extra_url
        """
        if filename not in _cached_links:
            # look for index urls
            with open(filename, 'r') as f:
                lines = f.read()
            urls = re.findall('^--extra-index-url (.*)$', lines, re.MULTILINE)
            _cached_links[filename] = urls
        return _cached_links[filename]

    requirements = []
    dependency_links = []
    reqs = parse_requirements(path, session=session)
    for req in reqs:
        requirements.append(str(req.req))
        filename = re.search('-r ([^\s]+)', req.from_path()).group(1)
        os.path.join(base_path, filename)
        urls = find_extra_url(filename)
        for url in urls:
            if not url.endswith('/'):
                url += '/'
            dependency_links.append(url + req.req.name)
    return requirements, dependency_links


install_requires, dependency_links = read_requirements_file('requirements.txt')
setup(
    name='page_rank_engine',
    version="0.2.0",
    description='Page Rank Engine',
    license='MIT License',
    setup_requires=[],
    install_requires=install_requires,
    dependency_links=dependency_links,
    author='Jason X. Zhang',
    author_email="jason.xing.zhang@gmail.com",
    packages=find_packages(),
    platforms='any',
    include_package_data=True
)


