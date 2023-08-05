from homevee.exceptions import *
from homevee.items.Device.Sensor import Sensor
from homevee.utils import database
from homevee.utils.device_types import ZWAVE_SENSOR


class ZWaveSensor(Sensor):
    def __init__(self, name, icon, location, save_data, sensor_type, id=None, value=None):
        super(ZWaveSensor, self).__init__(name, icon, location, save_data, sensor_type, id=id, value=value)

    def get_device_type(self):
        return ZWAVE_SENSOR

    def delete(self, db=None):
        try:
            with db:
                cur = db.cursor()
                cur.execute("DELETE FROM ZWAVE_SENSOREN WHERE ID == :id'", {'id': self.id})

                cur.close()
            return True
        except:
            return False

    def save_to_db(self, db=None):
        try:
            if(db is None):
                db = database.get_database_con()

            with db:
                cur = db.cursor()
                #insert
                if(self.id is None or self.id == ""):
                    cur.execute("INSERT INTO ZWAVE_SENSOREN (RAUM, SHORTFORM, ICON, SAVE_DATA,"
                                "SENSOR_TYPE, VALUE) VALUES (:location, :name, :icon, :save_data,"
                                ":sensor_type)",
                                {'location': self.location, 'name': self.name, 'icon': self.icon,
                                 'save_data': self.save_data, 'sensor_type': self.sensor_type})
                #update
                else:
                    cur.execute("UPDATE ZWAVE_SENSOREN SET RAUM = :location, SHORTFORM = :name, ICON = :icon,"
                                "SAVE_DATA = :save_data, SENSOR_TYPE = :sensor_type, VALUE = :value"
                                "WHERE ID = :id",
                                {'location': self.location, 'name': self.name, 'icon': self.icon,
                                 'save_data': self.save_data, 'sensor_type': self.sensor_type,
                                 'value': self.value, 'id': self.id})

                cur.close()

                    # TODO add generated id to object
        except:
            raise DatabaseSaveFailedException("Could not save room to database")

    def build_dict(self):
        dict = {
            'name': self.name,
            'icon': self.icon,
            'value': self.value,
            'id': self.id,
            'location': self.location,
            'save_data': self.save_data,
            'sensor_type': self.sensor_type
        }
        return dict

    @staticmethod
    def load_all_ids_from_db(ids, db=None):
        return ZWaveSensor.load_all_from_db('SELECT * FROM ZWAVE_SENSOREN WHERE ID IN (%s)'
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
                item = ZWaveSensor(result['SHORTFORM'], result['ICON'], result['RAUM'], result['SAVE_DATA'],
                                     result['SENSOR_TYPE'], result['ID'], result['VALUE'])
                items.append(item)

            cur.close()

        return items

    @staticmethod
    def load_from_db(id, db=None):
        items = ZWaveSensor.load_all_ids_from_db([id], db)

        if ((len(items) == 0) or (str(items[0].id) != str(id))):
            raise ItemNotFoundException("Could not find zwave-sensor-id: " + id)
        else:
            return items[0]

    @staticmethod
    def load_all(db=None):
        return ZWaveSensor.load_all_from_db('SELECT * FROM ZWAVE_SENSOREN', {}, db)

    @staticmethod
    def create_from_dict(dict):
        try:
            name = dict['name']
            id = dict['id']
            location = dict['location']
            value = dict['value']
            icon = dict['icon']
            save_data = dict['save_data']
            sensor_type = dict['sensor_type']

            item = ZWaveSensor(name, icon, location, save_data, sensor_type, id, value)

            return item

        except:
            raise InvalidParametersException("Invalid parameters for ZWaveSensor.create_from_dict()")

    @staticmethod
    def get_all(location=None, db=None):
        devices = []

        all_devices = ZWaveSensor.load_all(db)

        if location is None or location == "all":
            # get all devices of all types
            return all_devices

        for device in all_devices:
            if str(device.location) == str(location.id):
                devices.append(device)

        return devices