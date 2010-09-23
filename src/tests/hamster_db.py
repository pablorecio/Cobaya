# -*- coding: utf-8 -*-
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
# Copyright (C) 2010, Pablo Recio Quijano <precio@yaco.es>                    #
###############################################################################

import os
import shutil
import sys
import tempfile
import unittest


from cobaya import config, hamster_db


class HamsterDBTests(unittest.TestCase):

    def setUp(self):
        # some monkey patching to simulate system and home directories
        self.temp_root = tempfile.mkdtemp(prefix='tmp-cobaya-tests-')
        self.prefix = os.path.join(self.temp_root, 'usr')
        self.old_prefix = sys.prefix
        sys.prefix = self.prefix

        def custom_expand_user(not_used):
            return os.path.join(self.temp_root, 'home', 'user')

        self.old_expanduser = os.path.expanduser
        os.path.expanduser = custom_expand_user

        # create directories
        os.makedirs(os.path.expanduser(''))
        os.makedirs(os.path.join(self.temp_root, 'etc'))
        shutil.copy('./src/tests/hamster-test.db',
                    os.path.join(self.temp_root,
                        'home', 'user', 'hamster-test.db'))

        self.conf = config.Config()
        self.write_user_conf("""
[hamster]
db = ~/hamster-test.db
""")
        self.conf.load()

    def tearDown(self):
        shutil.rmtree(self.temp_root)
        sys.prefix = self.old_prefix
        os.path.expanduser = self.old_expanduser

    def _write_file(self, filename, conf):
        with open(filename, 'w') as f:
            f.write(conf)

    def write_user_conf(self, conf):
        self._write_file(os.path.join(self.temp_root,
                                      'home', 'user', '.cobayarc'), conf)

    def test_database_load(self):
        db = hamster_db.HamsterDB(self.conf)
        categories = {1: u'Trabajo',
                      2: u'Día a día',
                      3: u'foo-project',
                      4: u'bar-project',
                      5: u'egg-project',
                      -1: u'None', }
        tags = {1: u'awesome-tag',
                2: u'not-so-awesome-tag', }

        self.assertEquals(categories, db.categories)
        self.assertEquals(tags, db.tags)
