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


class NoHamsterData(Exception):

    def __init__(self, table, id):
        self.table = table
        self.id = id

    def __str__(self):
        return "No result for id '%s' on table '%s'" % (self.id, self.table)


class HamsterDB(object):

    def __init__(self, conf):
        db_filepath = conf.get_option('hamster.db')
        self.connection = sqlite3.connect(db_filepath)

        facts_result = self._query("SELECT id FROM facts")
        self.all_facts_id = [i[0] for i in facts_result]

        categories_result = self._query("SELECT id, name FROM categories")
        self.categories = dict([(cat_id, cat_name)
                                for cat_id, cat_name in categories_result])
        self.categories[-1] = 'None'

        tags_result = self._query("SELECT id, name FROM tags")
        self.tags = dict([(tag_id, tag_name)
                          for tag_id, tag_name in tags_result])

    def _query(self, query_str):
        cursor = self.connection.cursor()
        cursor.execute(query_str)
        return cursor.fetchall()

    def get_fact_by_id(self, fact_id):
        """ Obtains fact data by it's id.

        As the fact is unique, it returns a tuple like:
        (activity_id, start_time, end_time, description).
        If there is no fact with id == fact_id, a NoHamsterData
        exception will be raise
        """

        columns = 'activity_id, start_time, end_time, description'

        query = "SELECT %s FROM facts WHERE id = %s"
        result = self._query(query % (columns, fact_id))

        if result:
            return result[0]  # there only one fact with the id
        else:
            raise NoHamsterData('facts', fact_id)

    def get_activity_by_id(self, activity_id):
        """ Obtains activity data by it's id.

        As the activity is unique, it returns a tuple like:
        (name, category_id). If there is no activity with
        id == activity_id, a NoHamsterData exception will be raise
        """

        columns = 'name, category_id'

        query = "SELECT %s FROM activities WHERE id = %s"
        result = self._query(query % (columns, activity_id))

        if result:
            return result[0]  # there only one fact with the id
        else:
            raise NoHamsterData('activities', activity_id)

    def get_tags_by_fact_id(self, fact_id):
        """ Obtains the tags associated by a fact_id.

        This function returns a list of the tags name associated
        to a fact, such as ['foo', 'bar', 'eggs'].
        If the fact has no tags, it will return a empty list.
        If there are no fact with id == fact_id, a NoHamsterData
        exception will be raise
        """
        check_query = "SELECT id FROM facts WHERE id = %s"
        if not self._query(check_query % fact_id):
            raise NoHamsterData('facts', fact_id)

        query = "SELECT tag_id FROM fact_tags WHERE fact_id = %s"
        return [self.tags[row[0]] for row in self._query(query % fact_id)]

    def close_connection(self):
        self.connection.close()
