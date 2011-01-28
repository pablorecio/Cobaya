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

import json

from ConfigParser import NoOptionError


class RemoteTask(object):
    """ Represent a task ready to be send to a remote server
    """

    def __init__(self, task_id, ticket_number, project,
                 date, time, description, conf, remote_sync=False):

        self.task_id = task_id
        self.date = date
        self.time = time / 60 / 60  # in hours
        self.remote_sync = remote_sync
        self.ticket_number = ticket_number
        if isinstance(project, list):
            self.project = project[0]
        else:
            self.project = project
        self.conf = conf
        self.description = description

    def to_dict(self):
        data = {'ticket': self.ticket_number,
                'project': self.project_name(self.project),
                'date': self.date, 'time': self.time,
                'task_id': self.task_id,
                'description': self.description}
        return data

    def to_json(self):
        return json.dumps(self.to_dict())

    def project_name(self, project):
        if self.conf.parser.has_section('synonyms'):
            try:
                return self.conf.get_option("synonyms.%s" % project)
            except NoOptionError:
                pass
        return project
