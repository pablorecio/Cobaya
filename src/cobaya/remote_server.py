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

import httplib2
import json


class RemoteServer(object):

    def __init__(self, conf):
        self.url = conf.get_option('remote.url')
        user = conf.get_option('remote.user')
        passwd = conf.get_option('remote.password')

        self.http = httplib2.Http()
        self.http.add_credentials(user, passwd)

    def send_tasks(self, data):
        responses = {}
        responses['accepted'] = []
        responses['duplicated'] = []
        responses['rejected'] = []
        responses['not_found'] = []
        responses['server_error'] = []
        for task in data:
            if task['project'] == 'cice-buscador':
                task['project'] = 'CICE-buscador'
            if task['project'] == 'cice-parser':
                task['project'] = 'CICE-parser'
            json_data = json.dumps(task)
            response = self.http.request(method="POST",
                                         uri=self.url,
                                         headers={'content-type':
                                                  'application/json'},
                                         body=json_data)

            if response[0]['status'] == '200':
                responses['accepted'].append(task)
            elif response[0]['status'] == '400':  # bad request
                responses['rejected'].append(task)
            elif response[0]['status'] == '404':  # not found
                responses['not_found'].append(task)
            elif response[0]['status'] == '409':  # conflict
                responses['duplicated'].append(task)
            elif response[0]['status'] == '500':  # server error
                responses['server_error'].append(task)

        return responses
