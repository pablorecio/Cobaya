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

import os
import shutil
import sys
import tempfile
import unittest


import cobaya.config


class ConfigTests(unittest.TestCase):

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

    def tearDown(self):
        shutil.rmtree(self.temp_root)
        sys.prefix = self.old_prefix
        os.path.expanduser = self.old_expanduser

    def _write_file(self, filename, conf):
        with open(filename, 'w') as f:
            f.write(conf)

    def write_system_conf(self, conf):
        self._write_file(os.path.join(self.temp_root,
                                      'etc', 'cobaya.conf'),conf)

    def write_user_conf(self, conf):
        self._write_file(os.path.join(self.temp_root,
                                      'home', 'user', '.cobayarc'), conf)

    def write_conf(self, filename, conf):
        self._write_file(os.path.join(self.temp_root, filename), conf)

    def test_config_loading(self):
        conf = cobaya.config.Config()
        # test only default conf
        conf.load()
        user_path = os.path.join(self.temp_root, 'home', 'user')
        hamster_base_path = os.path.join(user_path, '.local', 'share',
                                         'hamster-applet')
        self.assertEquals(conf.get_option('hamster.db'),
                          os.path.join(hamster_base_path, 'hamster.db'))
        self.assertEquals(conf.get_option('hamster.log_file'),
                          os.path.join(hamster_base_path, 'synced-tasks.dat'))
        
        self.assertEquals(conf.get_option('remote.url'), '')
        self.assertEquals(conf.get_option('remote.user'), '')
        self.assertEquals(conf.get_option('remote.password'), '')

        self.assertEquals(conf.get_option('tasks.ticket_field'),
                          'activity')
        self.assertEquals(conf.get_option('tasks.project_field'),
                          'tags')
        self.assertEquals(conf.get_option('tasks.description_field'),
                          'description')
        self.assertEquals(conf.get_option('tasks.security_days'),
                          '10')


        # then add a system wide conf
        self.write_system_conf("""
[hamster]
db = /var/hamster/hamster.db

[remote]
url = http://www.example.com/web-service/hamster

[tasks]
security_days = 5
""")
        conf.load()
        self.assertEquals(conf.get_option('hamster.db'),
                          '/var/hamster/hamster.db')
        self.assertEquals(conf.get_option('remote.url'),
                          'http://www.example.com/web-service/hamster')
        self.assertEquals(conf.get_option('tasks.security_days'),
                          '5')


        # add user conf
        self.write_user_conf("""
[hamster]
db = ~/.hamster.db

[remote]
user = foo
password = bar
""")
        conf.load()
        self.assertEquals(conf.get_option('hamster.db'),
                          os.path.join(user_path, '.hamster.db'))
        self.assertEquals(conf.get_option('remote.url'),
                          'http://www.example.com/web-service/hamster')
        self.assertEquals(conf.get_option('remote.user'), 'foo')
        self.assertEquals(conf.get_option('remote.password'), 'bar')

        # add custom conf
        self.write_conf("custom.conf", """
[remote]
extra = special-conf
""")
        conf.load(os.path.join(self.temp_root, "custom.conf"))
        self.assertEquals(conf.get_option('hamster.db'),
                          os.path.join(user_path, '.hamster.db'))
        self.assertEquals(conf.get_option('remote.url'),
                          'http://www.example.com/web-service/hamster')
        self.assertEquals(conf.get_option('remote.user'), 'foo')
        self.assertEquals(conf.get_option('remote.password'), 'bar')
        self.assertEquals(conf.get_option('remote.extra'), 'special-conf')


    def test_get_option(self):
        conf = cobaya.config.Config()

        self.write_system_conf("""
[hamster]
db = /var/hamster/hamster.db

[remote]
url = http://www.example.com/web-service/hamster
""")
        conf.load()

        self.assertEquals(conf.get_option('hamster.db'),
                          '/var/hamster/hamster.db')
        self.assertRaises(cobaya.config.ConfigError,
                          conf.get_option, 'too.much.dots')
        self.assertRaises(cobaya.config.ConfigError,
                          conf.get_option, 'too-few-dots')
        self.assertRaises(cobaya.config.ConfigError,
                          conf.get_option, '')

if __name__ == '__main__':
    unittest.main()
