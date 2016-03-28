#!/usr/bin/env python3
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
"""Setup file for dpcs-client."""

from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        raise SystemExit(errno)

setup(classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: ' +
        'GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: Log Analysis',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Software Distribution',
        'Topic :: Utilities'
      ],
      scripts=['main/dpcs', 'settings/dpcs-settings'],
      cmdclass={'test': PyTest},
      description='The client for the Data Powered Crash Solver',
      install_requires=['requests', 'pgi'],
      keywords=['dpcs', 'ai', 'fix', 'error solving', 'log analysis'],
      license='LGPLv3',
      long_description=open('../readme.md', 'r').read(),
      name='dpcs',
      packages=[],
      tests_require=['pytest', 'coverage'],
      url='https://github.com/DPCS-team/DPCS',
      version='0.1.0'
      )
