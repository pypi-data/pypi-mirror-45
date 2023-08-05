import traceback

from homevee.DeviceAPI.zwave.utils import do_zwave_request
from homevee.Helper import Logger
from homevee.exceptions import DatabaseSaveFailedException, ItemNotFoundException, InvalidParametersException
from homevee.items.Device.Thermostat import Thermostat
from homevee.utils import database
from homevee.utils.device_types import ZWAVE_THERMOSTAT


class ZWaveThermostat(Thermostat):
    def __init__(self, name, icon, location, id=None, temp=None):
        super(ZWaveThermostat, self).__init__(name, icon, location, id=id, temp=temp)

    def get_device_type(self):
        return ZWAVE_THERMOSTAT

    def delete(self, db=None):
        try:
            with db:
                cur = db.cursor()
                cur.execute("DELETE FROM ZWAVE_THERMOSTATS WHERE ID == :id'", {'id': self.id})

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
                cur.execute("""INSERT OR IGNORE INTO ZWAVE_THERMOSTATS (THERMOSTAT_ID, NAME, ICON, VALUE, RAUM) VALUES 
                            (:id, :name, :icon, :last_temp, :room)""",
                            {'id': self.id, 'name': self.name, 'icon': self.icon,
                             'last_temp': self.temp, 'room': self.location})
                # update
                cur.execute("""UPDATE OR IGNORE ZWAVE_THERMOSTATS SET NAME = :name, ICON = :icon,
                            VALUE = :last_temp, RAUM = :room WHERE THERMOSTAT_ID = :id""",
                            {'name': self.name, 'icon': self.icon, 'last_temp': self.temp,
                             'room': self.location, 'id': self.id})

                cur.close()

                # TODO add generated id to object
        except:
            if(Logger.IS_DEBUG):
                traceback.print_exc()
            raise DatabaseSaveFailedException("Could not save max-thermostat to database")

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
            result = do_zwave_request("/ZAutomation/api/v1/devices/" + str(self.id)
                                      + "/command/exact?level=" + str(temp),db)
            if result is not None and result['code'] == 200:
                return True
            else:
                return False
        except:
            if(Logger.IS_DEBUG):
                traceback.print_exc()
            return False

    @staticmethod
    def load_all_ids_from_db(ids, db=None):
        return ZWaveThermostat.load_all_from_db('SELECT * FROM MAX_THERMOSTATS WHERE ID IN (%s)'
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
                item = ZWaveThermostat(result['NAME'], result['ICON'], result['RAUM'], result['THERMOSTAT_ID'],
                                     result['VALUE'])
                items.append(item)

            cur.close()

        return items

    @staticmethod
    def load_from_db(id, db=None):
        items = ZWaveThermostat.load_all_ids_from_db([id], db)

        if ((len(items) == 0) or (str(items[0].id) != str(id))):
            raise ItemNotFoundException("Could not find zwave-thermostat-id: " + id)
        else:
            return items[0]

    @staticmethod
    def load_all(db=None):
        return ZWaveThermostat.load_all_from_db('SELECT * FROM ZWAVE_THERMOSTATS', {}, db)

    @staticmethod
    def create_from_dict(dict):
        try:
            name = dict['name']
            id = dict['id']
            location = dict['location']
            temp = dict['temp']
            icon = dict['icon']

            item = ZWaveThermostat(name, icon, location, id, temp)

            return item

        except:
            raise InvalidParametersException("Invalid parameters for ZWaveThermostat.create_from_dict()")

    @staticmethod
    def get_all(location=None, db=None):
        devices = []

        all_devices = ZWaveThermostat.load_all(db)

        if location is None or location == "all":
            # get all devices of all types
            return all_devices

        for device in all_devices:
            if str(device.location) == str(location.id):
                devices.append(device)

        return devices