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

import getpass
import urlparse

HAS_GNOME_KEYRING_SUPPORT = None

try:
    import gnomekeyring
    HAS_GNOME_KEYRING_SUPPORT = True
except ImportError:
    HAS_GNOME_KEYRING_SUPPORT = False


def get_app():
    return 'Cobaya'


def get_password(config):
    """Returns the password for a remote server

    It tries to fetch the password from the following
    locations in this order:

     1. config file [remote] section, password option
     2. GNOME keyring
     3. interactively, from the user
    """
    password = config.get_option('remote.password')

    if password == '':
        user = config.get_option('remote.user')
        url = config.get_option('remote.url')
        url_obj = urlparse.urlparse(url)
        server = url_obj.hostname
        protocol = url_obj.scheme

        if HAS_GNOME_KEYRING_SUPPORT:
            password = get_password_from_gnome_keyring(user, server, protocol)

        else:
            prompt = 'Enter %s password for %s at %s: ' % (get_app(), user,
                                                           server)
            password = getpass.getpass(prompt)

    return password


def get_password_from_gnome_keyring(user, server, protocol):
    try:
        results = gnomekeyring.find_network_password_sync(user=user,
                                                          server=server,
                                                          protocol=protocol)
        return results[0]['password']
    except gnomekeyring.NoMatchError:
        return set_password_in_gnome_keyring(user, server, protocol)


def set_password_in_gnome_keyring(user, server, protocol):
    print 'It looks like this is the first time you run %s' % get_app()
    print 'with the user "%s" at server "%s" using protocol "%s"' % (user,
                                                                     server,
                                                                     protocol)
    password_match = False
    while not password_match:
        password1 = getpass.getpass('Enter password: ')
        password2 = getpass.getpass('Enter password again: ')
        password_match = password1 == password2
        if not password_match:
            print 'Passwords do not match. Please, enter them again'

    keyring = gnomekeyring.get_default_keyring_sync()
    display_name = '%s password for %s at %s' % (get_app(), user, server)
    attrs = {'user': user, 'server': server, 'protocol': protocol}
    gnomekeyring.item_create_sync(keyring, gnomekeyring.ITEM_NETWORK_PASSWORD,
                                  display_name, attrs, password1, False)
    return password1
