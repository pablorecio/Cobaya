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

import sqlite3

import settings


def get_all_tasks():
    """Returns a list with every task registred on Hamster.
    """
    facts = _get_facts()
    activities = _get_activities()
    tags = _get_tags()
    categories = _get_categories()
    tasks = []
    for key in facts:
        task = {}
        activity = activities[facts[key]['activity_id']]
        task['name'] = activity['name']
        task['category'] = categories[activity['category_id']]
        task['tags'] = []
        for tag_id in facts[key]['tags_id']:
            task['tags'].append(tags[tag_id])
        task['start_date'] = facts[key]['start_date']
        task['end_date'] = facts[key]['end_date']
        tasks.append(task)

    return tasks

def _get_tags():
    """Returns a dictionary with the existing tags on Hamster.
    """
    
    conn = sqlite3.connect(settings.HAMSTER_APPLET_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tags")
    tag_list = cursor.fetchall()
    tags = {}
    for tag in tag_list:
        tags[tag[0]] = tag[1]
    conn.close()

    return tags


def _get_categories():
    """Returns a dictionary with the existing categories on Hamster.
    """

    conn = sqlite3.connect(settings.HAMSTER_APPLET_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categories")
    category_list = cursor.fetchall()
    categories = {}
    for category in category_list:
        categories[category[0]] = category[4]
    conn.close()

    return categories


def _get_activities():
    """Returns a dictionary with the existing activities on Hamster
    """

    conn = sqlite3.connect(settings.HAMSTER_APPLET_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM activities")
    activity_list = cursor.fetchall()
    activities = {}
    for activity in activity_list:
        activities[activity[0]] = {'name': activity[6],
                                   'category_id': activity[5]}
    conn.close()

    return activities


def _get_facts():
    """Returns a dictionary with the existing facts on Hamster
    """

    conn = sqlite3.connect(settings.HAMSTER_APPLET_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM facts")
    fact_list = cursor.fetchall()
    facts = {}
    for fact in fact_list:
        facts[fact[0]] = {'activity_id': fact[1],
                          'start_date': fact[2],
                          'end_date': fact[3],
                          'tags_id': []}

    cursor.execute("SELECT * FROM fact_tags")
    fact_tags = cursor.fetchall()
    for i in fact_tags:
        facts[i[0]]['tags_id'].append(i[1])

    conn.close()

    return facts
