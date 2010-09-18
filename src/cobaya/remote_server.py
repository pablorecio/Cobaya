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

import logging

LOG_FILENAME = 'cobaya.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)


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
            json_data = json.dumps(task)
            response, content = self.http.request(
                method="POST",
                uri=self.url,
                headers={'content-type': 'application/json'},
                body=json_data,
                )

            status_table = {
                '200': ('accepted', logging.info,
                        "Ticket %s of %s project done on %s synced"),
                '400': ('rejected', logging.error,  # bad request
                        "Ticket %s of %s project done on %s "
                        "is not allowed on the webservice"),
                '404': ('not_found', logging.error,
                        "Ticket %s of %s project done on %s "
                        "is not found on the webservice"),
                '409': ('duplicated', logging.warning,  # conflict
                        "Ticket %s of %s project done on %s "
                        "is already register"),
                '500': ('server_error', None, None),
                }

            try:
                where, log, msg = status_table[response['status']]
                responses[where].append(task)
                if msg is not None:
                    ticket_project_date = (task['ticket'], task['project'],
                                           task['date'])
                    log(msg % ticket_project_date)
            except KeyError:
                logging.error("The server returned a status "
                              "I do not know how to handle")

        return responses
