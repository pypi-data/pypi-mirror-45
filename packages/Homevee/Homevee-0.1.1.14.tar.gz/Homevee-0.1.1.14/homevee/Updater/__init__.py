import json
import os
import urllib
from _thread import start_new_thread

import pip
from packaging import version

from homevee.Helper.helper_functions import has_permission
from homevee.utils import constants, firebase_utils, database


def get_homevee_update_version():
    installed_version = constants.HOMEVEE_VERSION_NUMBER

    newest_version = get_newest_version()

    if(newest_version is None):
        return False

    if(version.parse(newest_version) > version.parse(installed_version)):
        return newest_version
    else:
        return None

def get_newest_version():
    url = "https://pypi.org/pypi/Homevee/json"

    try:
        response = urllib.request.urlopen(url).read()
        response = response.decode('utf-8')
        response_json = json.loads(response)
        version = response_json['info']['version']

        return version
    except:
        return None

def check_for_updates():
    new_version = get_homevee_update_version()

    return {
        'updates':{
            'current_version': constants.HOMEVEE_VERSION_NUMBER,
            'new_version': new_version,
            'update_available': (new_version is not None),
            'changelog': "Changelog blabla..." #TODO add changelog or link to actual changelog
        }
    }

'''
Updates the Homevee PIP-Package
Returns true if update was successful,
returns false if there was an error
'''
def do_homevee_update(username, db):
    if(not has_permission(username, "admin", db)):
        return {'error': "nopermission"}

    start_new_thread(update_thread, ())

    return {'result': 'ok'}

def update_thread():
    new_version = get_homevee_update_version()

    try:
        pip.main(["install", "--upgrade", "Homevee"])
    except:
        return False

    # TODO texte lokalisieren
    title = "Update"
    body = "Update auf Version " + new_version

    # Send notification to admin
    firebase_utils.send_notification_to_admin(title, body, database.get_database_con())

    # Reboot the system after the update
    os.system('reboot')