import json
import traceback
import urllib.request

from homevee.Helper import Logger
from homevee.exceptions import DatabaseSaveFailedException
from homevee.items.Device.Thermostat import Thermostat
from homevee.items.Gateway import *
from homevee.utils.device_types import RADEMACHER_THERMOSTAT


class RademacherThermostat(Thermostat):
    def __init__(self, name, icon, location, id=None, temp=None):
        super(RademacherThermostat, self).__init__(name, icon, location, id=id, temp=temp)

    def get_device_type(self):
        return RADEMACHER_THERMOSTAT

    def delete(self, db=None):
        try:
            with db:
                cur = db.cursor()
                cur.execute("DELETE FROM HOMEPILOT_THERMOSTATS WHERE ID == :id'", {'id': self.id})

                cur.close()
            return True
        except:
            return False

    def save_to_db(self, db=None):
        try:
            if (db is None):
                db = database.get_database_con()

            with db:
                cur = db.cursor()
                # insert
                cur.execute("""INSERT OR IGNORE INTO HOMEPILOT_THERMOSTATS (ID, NAME, ICON, LAST_TEMP, ROOM) VALUES 
                            (:id, :name, :icon, :last_temp, :room)""",
                            {'id': self.id, 'name': self.name, 'icon': self.icon,
                             'last_temp': self.temp, 'room': self.location})
                # update
                cur.execute("""UPDATE OR IGNORE HOMEPILOT_THERMOSTATS SET NAME = :name, ICON = :icon,
                            LAST_TEMP = :last_temp, ROOM = :room WHERE ID = :id""",
                            {'name': self.name, 'icon': self.icon, 'last_temp': self.temp,
                             'room': self.location, 'id': self.id})

                cur.close()

                # TODO add generated id to object
        except:
            if(Logger.IS_DEBUG):
                traceback.print_exc()
            raise DatabaseSaveFailedException("Could not save homepilot-thermostat to database")

    def build_dict(self):
        dict = {
            'name': self.name,
            'icon': self.icon,
            'id': self.id,
            'temp': self.temp,
            'location': self.location
        }
        return dict

    def update_temp(self, temp, db=None):
        try:
            gateway = Gateway.load_from_db(RADEMACHER_HOMEPILOT, db)

            value = int(float(temp) * 10)

            url = "http://" + gateway.ip + "/deviceajax.do?cid=9&did=" + str(self.id) + "&goto=" + str(value) + "&command=0"

            response = urllib.request.urlopen(url).read()

            data = json.loads(response)

            if (data['status'] != 'uisuccess'):
                return False
            return True
        except:
            if Logger.IS_DEBUG:
                traceback.print_exc()
        return False

    @staticmethod
    def load_all_ids_from_db(ids, db=None):
        return RademacherThermostat.load_all_from_db('SELECT * FROM HOMEPILOT_THERMOSTATS WHERE ID IN (%s)'
                                              % ','.join('?' * len(ids)), ids, db)

    @staticmethod
    def load_all_from_db(query, params, db=None):
        if (db is None):
            db = database.get_database_con()

        items = []

        with db:
            cur = db.cursor()

            cur.execute(query, params)
            for result in cur.fetchall():
                item = RademacherThermostat(result['NAME'], result['ICON'], result['ROOM'], result['ID'],
                                     result['LAST_TEMP'])
                items.append(item)

            cur.close()

        return items

    @staticmethod
    def load_from_db(id, db=None):
        items = RademacherThermostat.load_all_ids_from_db([id], db)

        if ((len(items) == 0) or (str(items[0].id) != str(id))):
            raise ItemNotFoundException("Could not find homepilot-thermostat-id: " + id)
        else:
            return items[0]

    @staticmethod
    def load_all(db=None):
        return RademacherThermostat.load_all_from_db('SELECT * FROM HOMEPILOT_THERMOSTATS', {}, db)

    @staticmethod
    def create_from_dict(dict):
        try:
            name = dict['name']
            id = dict['id']
            location = dict['location']
            temp = dict['temp']
            icon = dict['icon']

            item = RademacherThermostat(name, icon, location, id, temp)

            return item

        except:
            raise InvalidParametersException("Invalid parameters for RademacherThermostat.create_from_dict()")

    @staticmethod
    def get_all(location=None, db=None):
        devices = []

        all_devices = RademacherThermostat.load_all(db)

        if location is None or location == "all":
            # get all devices of all types
            return all_devices

        for device in all_devices:
            if str(device.location) == str(location.id):
                devices.append(device)

        return devices