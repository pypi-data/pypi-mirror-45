import urllib.request

from homevee.exceptions import *
from homevee.items.Device.Switch import Switch
from homevee.items.Gateway import Gateway, FUNKSTECKDOSEN_CONTROLLER
from homevee.utils import database
from homevee.utils.device_types import FUNKSTECKDOSE


class Funksteckdose(Switch):
    def __init__(self, name, icon, location, home_code, socket_number, id=None, mode=False):
        super(Funksteckdose, self).__init__(name, icon, location, id=id, mode=mode)
        self.home_code = home_code
        self.socket_number = socket_number

    def get_device_type(self):
        return FUNKSTECKDOSE

    def delete(self, db=None):
        try:
            with db:
                cur = db.cursor()
                cur.execute("DELETE FROM FUNKSTECKDOSEN WHERE DEVICE == :id'", {'id': self.id})

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
                    cur.execute("INSERT INTO FUNKSTECKDOSEN (ROOM, NAME, ICON, HAUSCODE, STECKDOSENNNUMMER) "
                                "VALUES (:location, :name, :icon, :home_code, :socket_number)",
                                {'location': self.location, 'name': self.name, 'icon': self.icon,
                                 'home_code': self.home_code, 'socket_number': self.socket_number})
                #update
                else:
                    cur.execute("UPDATE FUNKSTECKDOSEN SET ROOM = :location, NAME = :name, ICON = :icon,"
                                "HAUSCODE = :home_code, STECKDOSENNUMMER = :socket_number, ZUSTAND = :mode"
                                "WHERE DEVICE = :id",
                                {'location': self.location, 'name': self.name, 'icon': self.icon,
                                 'home_code': self.home_code, 'socket_number': self.socket_number,
                                 'mode': self.mode, 'id': self.id})

                cur.close()

                    # TODO add generated id to object
        except:
            raise DatabaseSaveFailedException("Could not save room to database")

    def build_dict(self):
        dict = {
            'name': self.name,
            'icon': self.icon,
            'home_code': self.home_code,
            'socket_number': self.socket_number,
            'id': self.id,
            'mode': self.mode,
            'location': self.location
        }
        return dict

    def update_mode(self, mode, db=None):
        try:
            gateway = Gateway.load_from_db(FUNKSTECKDOSEN_CONTROLLER)

            url = 'http://' + str(gateway.ip) + '/funksteckdose.php?hauscode=' + str(self.home_code) + \
                  '&steckdosennummer=' + str(self.socket_number) + "&zustand=" + str(mode)
            #Logger.log(url)
            result = urllib.request.urlopen(url)

            return True

        except:
            return False

    @staticmethod
    def load_all_ids_from_db(ids, db=None):
        return Funksteckdose.load_all_from_db('SELECT * FROM FUNKSTECKDOSEN WHERE DEVICE IN (%s)'
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
                item = Funksteckdose(result['NAME'], result['ICON'], result['ROOM'], result['HAUSCODE'],
                                     result['STECKDOSENNUMMER'], result['DEVICE'], result['ZUSTAND'])
                items.append(item)

            cur.close()

        return items

    @staticmethod
    def load_from_db(id, db=None):
        items = Funksteckdose.load_all_ids_from_db([id], db)

        if ((len(items) == 0) or (str(items[0].id) != str(id))):
            raise ItemNotFoundException("Could not find funksteckdosen-id: " + id)
        else:
            return items[0]

    @staticmethod
    def load_all(db=None):
        return Funksteckdose.load_all_from_db('SELECT * FROM FUNKSTECKDOSEN', {}, db)

    @staticmethod
    def create_from_dict(dict):
        try:
            name = dict['name']
            id = dict['id']
            location = dict['location']
            home_code = dict['home_code']
            socket_number = dict['socket_number']
            mode = dict['mode']
            icon = dict['icon']

            funksteckdose = Funksteckdose(name, icon, location, home_code, socket_number, id, mode)

            return funksteckdose

        except:
            raise InvalidParametersException("Invalid parameters for Funksteckdose.create_from_dict()")

    @staticmethod
    def get_all(location=None, db=None):
        devices = []

        all_devices = Funksteckdose.load_all(db)

        if location is None or location == "all":
            # get all devices of all types
            return all_devices

        for device in all_devices:
            if str(device.location) == str(location.id):
                devices.append(device)

        return devices