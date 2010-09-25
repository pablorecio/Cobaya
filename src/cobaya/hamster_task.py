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
""" This module provides some classes to extract data from Hamster DB and
convert it to easy-to-handle data"""

import re
from datetime import datetime

from cobaya.hamster_db import HamsterDB
from cobaya.remote_task import RemoteTask


class HamsterTask(object):
    """ Represent a task in Hamster.

    A task is a single record on Hamster, with:
      * activity name
      * category
      * tags
      * start and end datetime
      * time expended
    """

    def __init__(self, fact_id, conf):

        self.id = fact_id
        self.conf = conf

        db = HamsterDB(self.conf)

        (activity_id, self.start_time,
         self.end_time, self.description) = db.get_fact_by_id(self.id)

        if self.end_time:
            self.elapsed_time = _elapsed_time(self.start_time, self.end_time)
        else:
            self.elapsed_time = 0.0

        (self.activity, category_id) = db.get_activity_by_id(activity_id)
        self.category = db.categories[category_id]

        self.tags = db.get_tags_by_fact_id(self.id)

        if len(self.tags) > 0:
            self.tag = self.tags[0] or ''  # first tag
        else:
            self.tag = ''

        db.close_connection()

    def __str__(self):
        tags_repr = ', '.join(self.tags)
        return u"[%s@%s] %s - %s [%s]" % (self.activity, self.category,
                                          self.start_time, self.end_time,
                                          tags_repr)

    def get_remote_task(self):
        ticket_field = self.conf.get_option('tasks.ticket_field')
        project_field = self.conf.get_option('tasks.project_field')
        description_field = self.conf.get_option('tasks.description_field')

        dict_data = self.__dict__
        description = dict_data[description_field]
        project_name = dict_data[project_field]
        ticket_pattern = re.compile('#\d+')
        ticket_match = ticket_pattern.search(dict_data[ticket_field])
        if ticket_match:
            ticket_number = int(ticket_match.group()[1:])
        else:
            ticket_number = 0

        return RemoteTask(self.id, ticket_number, project_name,
                          self.start_time[:10], self.elapsed_time,
                          description)


def _elapsed_time(begin_time, end_time):
    """Assuming format YYYY-MM-DD hh:mm:ss

    Returns the elapsed time in seconds
    """
    bt = datetime.strptime(begin_time, "%Y-%m-%d %H:%M:%S")
    et = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

    return float((et - bt).seconds)
