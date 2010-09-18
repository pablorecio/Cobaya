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
# Copyright (C) 2010, Pablo Recio Quijano, <precio@yaco.es>                   #
###############################################################################

import sqlite3


class HamsterDB(object):

    def __init__(self, conf):
        db_filepath = conf.get_option('hamster.db')
        self.connection = sqlite3.connect(db_filepath)

        categories_result = self.query("SELECT id, name FROM categories")
        self.categories = {-1: 'None'}
        for cat_id, cat_name in categories_result:
            self.categories[cat_id] = cat_name

        tags_result = self.query("SELECT id, name FROM tags")
        self.tags = {}
        for tag_id, tag_name in tags_result:
            self.tags[tag_id] = tag_name

    def query(self, query_str):
        cursor = self.connection.cursor()
        cursor.execute(query_str)
        return cursor.fetchall()

    def close_connection(self):
        self.connection.close()
