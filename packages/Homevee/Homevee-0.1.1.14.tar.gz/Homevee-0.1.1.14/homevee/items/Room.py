from homevee.exceptions import RoomNotFoundException, InvalidParametersException, DatabaseSaveFailedException
from homevee.items import Item
from homevee.utils import database


class Room(Item):
    def __init__(self, name, icon, id=None):
        super(Room, self).__init__()
        self.id = id
        self.name = name
        self.icon = icon

    def get_room_data(self, db):
        if(self.room_data is None):
            room_data = None #TODO load room data

            self.room_data = room_data

        return room_data

    def delete(self, db=None):
        pass

    def save_to_db(self, db=None):
        try:
            if(db is None):
                db = database.get_database_con()

            #with db:
            #    cur = db.cursor()
            #    #insert
            #    if(self.id is None or self.id == ""):
            #        cur.execute("INSERT INTO ROOMS (NAME, ICON) VALUES (:name, :icon)",
            #                    {'name': self.name, 'icon': self.icon})
            #    #update
            #    else:
            #        cur.execute("UPDATE ROOMS SET NAME = :name, ICON = :icon WHERE LOCATION = :id",
            #                    {'name': self.name, 'icon': self.icon, 'id': self.id})
            #        # TODO add generated id to object
        except:
            raise DatabaseSaveFailedException("Could not save room to database")

    def get_dict(self, fields=None):
        dict = {
            'id': self.id,
            'name': self.name,
            'icon': self.icon
        }

        if(fields is None):
            return dict
        else:
            try:
                output_dict = {}

                for field in fields:
                    output_dict[field] = dict[field]

                return output_dict
            except:
                raise InvalidParametersException("InvalidParams given for Room.get_dict()")







    @staticmethod
    def load_all_ids_from_db(ids, db=None):
        return Room.load_all_from_db('SELECT * FROM ROOMS WHERE LOCATION IN (%s)' % ','.join('?'*len(ids)),
                                     ids, db)

    @staticmethod
    def load_all_from_db(query, params, db=None):
        if (db is None):
            db = database.get_database_con()

        rooms = []

        with db:
            cur = db.cursor()

            cur.execute(query, params)

            for result in cur.fetchall():
                room = Room(result['NAME'], result['ICON'], result['LOCATION'])
                rooms.append(room)

        return rooms

    @staticmethod
    def get_name_by_id(id, db=None):
        room = Room.load_from_db(id, db)
        return room.name

    @staticmethod
    #ID is username
    def load_from_db(id, db=None):
        rooms = Room.load_all_ids_from_db([id], db)

        if((len(rooms) == 0) or (str(rooms[0].id) != str(id))):
            raise RoomNotFoundException("Could not find room with id: "+str(id))
        else:
            return rooms[0]

    @staticmethod
    def load_all(db=None):
        return Room.load_all_from_db('SELECT * FROM ROOMS', {}, db)

    @staticmethod
    def create_from_dict(dict):
        try:
            id = dict['id']
            name = dict['name']
            icon = dict['icon']

            room = Room(name, icon, id)

            return room
        except:
            raise InvalidParametersException("Room.create_from_dict(): invalid dict")