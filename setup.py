###############################################################################
# This program is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU General Public License as published by        #
# the Free Software Foundation, either version 3 of the License, or           #
# any later version.                                                          #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
#                                                                             #
# Copyright (C) 2010, Lorenzo Gil Sanchez, <lgs@yaco.es>                      #
###############################################################################

import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name="Cobaya",
    version="0.1dev",
    author="Pablo Recio Quijano",
    author_email="precio@yaco.es",
    description="Command line programm to send Hamster task to a remote system",
    long_description=(
        read('README')
        + '\n\n' +
        read('CHANGES')
        ),
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Utilities',
        ],
    license="GPL 3",
    keywords="hamster workreport",
    url='http://github.com/pyriku/Cobaya',

    packages=find_packages('src'),
    package_dir = {'': 'src'},
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'cobaya = cobaya.app:main',
            ]
        },
    test_suite="tests",
)
