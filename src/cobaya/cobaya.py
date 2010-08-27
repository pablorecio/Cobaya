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

"""This module provides functions to extract data from Hamster DB
"""

from hamster_task import HamsterTask
from hamster_db import HamsterDB


def get_all_tasks():
    """Returns a list with every task registred on Hamster.
    """

    db = HamsterDB()
    result = db.query("SELECT id FROM facts")
    db.close_connection()

    fact_list = [x[0] for x in result]
    tasks = []

    for fact_id in fact_list:
        tasks.append(HamsterTask(fact_id))

    return tasks
