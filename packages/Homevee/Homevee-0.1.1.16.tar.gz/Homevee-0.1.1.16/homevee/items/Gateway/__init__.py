from homevee.exceptions import ItemNotFoundException, InvalidParametersException, AbstractFunctionCallException
from homevee.items import Item
from homevee.utils import database

PHILIPS_HUE_BRIDGE = "Philips Hue"
Z_WAVE_GATEWAY = "Z-Wave"
FUNKSTECKDOSEN_CONTROLLER = "Funksteckdosen-Controller"
MAX_CUBE = "MAX! Cube"
MQTT_BROKER = "MQTT Broker"
MIYO_CUBE = "MIYO Cube"
RADEMACHER_HOMEPILOT = "Rademacher HomePilot"


class Gateway(Item):
    def __init__(self, name, ip, port, key1, key2, type):
        super(Gateway, self).__init__()
        self.name = name
        self.ip = ip
        self.port = port
        self.key1 = key1
        self.key2 = key2
        self.type = type

    def save_to_db(self, db=None):
        try:
            if db is None:
                db = database.get_database_con()

            with db:
                cur = db.cursor()

                cur.execute("""INSERT OR IGNORE INTO GATEWAYS (NAME, IP, PORT, KEY1, KEY2, TYPE) VALUES
                            (:name, :ip, :port, :key1, :key2, :type)""",
                            {'name': self.name, 'ip': self.ip, 'port': self.port,
                             'key1': self.key1, 'key2': self.key2, 'type': self.type})

                cur.execute("""UPDATE OR IGNORE GATEWAYS SET IP = :ip, PORT = :port, KEY1 = :key1,
                            KEY2 = :key2, TYPE = :type WHERE NAME = :name""",
                            {'ip': self.ip, 'port': self.port, 'key1': self.key1,
                             'key2': self.key2, 'type': self.type, 'name': self.name})

                return True
        except:
            return False

    def delete(self, db=None):
        try:
            with db:
                cur = db.cursor()
                cur.execute("DELETE FROM GATEWAYS WHERE NAME == :key", {'key': self.name})

                cur.close()
            return True
        except:
            return False

    def build_dict(self):
        dict = {
            'name': self.name,
            'ip': self.ip,
            'port': self.port,
            'key1': self.key1,
            'key2': self.key2,
            'type': self.type
        }
        return dict

    @staticmethod
    def load_all_ids_from_db(ids, db=None):
        return Gateway.load_all_from_db('SELECT * FROM GATEWAYS WHERE NAME IN (%s)' % ','.join('?' * len(ids)),
                                        ids, db)

    @staticmethod
    def load_all_from_db(query, params, db=None):
        if db is None:
            db = database.get_database_con()

        gateways = []

        with db:
            cur = db.cursor()

            cur.execute(query, params)

            for item in cur.fetchall():
                gateway = Gateway(item['NAME'], item['IP'], item['PORT'], item['KEY1'],
                                  item['KEY2'], item['TYPE'])
                gateways.append(gateway)

            cur.close()

        return gateways

    @staticmethod
    def load_from_db(id, db=None):
        items = Gateway.load_all_ids_from_db([id], db)

        if ((len(items) == 0) or (items[0].name != id)):
            raise ItemNotFoundException("Could not find gateway-id: " + id)
        else:
            return items[0]

    @staticmethod
    def create_from_dict(dict):
        try:
            name = dict['name']
            ip = dict['ip']
            port = dict['port']
            key1 = dict['key1']
            key2 = dict['key2']
            type = dict['type']

            gateway = Gateway(name, ip, port, key1, key2, type)

            return gateway
        except:
            raise InvalidParametersException("Invalid parameters for Gateway.create_from_dict()")

    def get_devices(self):
        raise AbstractFunctionCallException("Method Gateway.get_devices() is abstract")