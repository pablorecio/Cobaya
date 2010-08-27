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
# Copyright (C) 2010, Lorenzo Gil Sanchez <lgs@yaco.es>                       #
###############################################################################

"""Configuration management.
"""

import StringIO
import ConfigParser
import os
import sys

class ConfigError(Exception):
    pass


class Config(object):

    default_conf = """
[hamster]
db = ~/.local/share/hamster-applet/hamster.db

[remote]
url =
user =
password =
"""

    def __init__(self):
        self.parser = ConfigParser.SafeConfigParser()
        self.conf_files = [
            os.path.join(os.path.dirname(sys.prefix), 'etc', 'cobaya.conf'),
            os.path.join(os.path.expanduser('~'), '.cobayarc'),
            ]

    def load(self, filename=None):
        self.parser.readfp(StringIO.StringIO(self.default_conf))

        if filename is not None:
            self.conf_files.append(filename)

        return self.parser.read(self.conf_files)


    def get_option(self, option):
        parts = option.split('.')
        if not parts or len(parts) != 2:
            raise ConfigError("Options must be qualified with the section")

        section, option = parts
        value = self.parser.get(section, option)
        if value.startswith('~'):
            value =  value.replace('~', os.path.expanduser('~'))

        return value
