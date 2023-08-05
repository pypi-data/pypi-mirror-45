import traceback

from homevee.Helper import Logger
from homevee.exceptions import ItemNotFoundException, DatabaseSaveFailedException, InvalidParametersException
from homevee.items import Item
from homevee.utils import database


class Event(Item):
    def __init__(self, text, type, timestamp=None, id=None):
        super(Event, self).__init__()

        self.timestamp = timestamp
        self.text = text
        self.type = type
        self.id = id

    def delete(self, db=None):
        try:
            with db:
                cur = db.cursor()
                cur.execute("DELETE FROM EVENTS WHERE ID == :id'", {'id': self.id})

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
                if (self.id is None or self.id == ""):
                    cur.execute("""INSERT INTO EVENTS (TEXT, TYPE) VALUES (:text, :type)""",
                                {'text': self.text, 'type': self.type})
                # update
                else:
                    cur.execute("""UPDATE EVENTS SET TEXT = :text, TYPE = :type WHERE ID = :id""",
                                {'text': self.text, 'type': self.type, 'id': self.id})

                cur.close()

                #TODO add generated id to object
        except:
            if(Logger.IS_DEBUG):
                traceback.print_exc()
            raise DatabaseSaveFailedException("Could not save event to database")

    def build_dict(self):
        dict = {
            'id': self.id,
            'timestamp': self.timestamp,
            'text': self.text,
            'type': self.type
        }
        return dict

    @staticmethod
    def load_all_from_db(query, params, db=None):
        if (db is None):
            db = database.get_database_con()

        items = []

        with db:
            cur = db.cursor()

            cur.execute(query, params)
            for result in cur.fetchall():
                item = Event(result['TEXT'], result['TYPE'], result['TIMESTAMP'], result['ID'])
                items.append(item)

            cur.close()

        return items

    @staticmethod
    def load_all_from_db_desc_date_by_type(offset, limit, type=None, db=None):
        params = {'limit': limit, 'offset': offset}

        where_clause = ""

        if type is not None and type != "":
            params['type'] = type
            where_clause = "WHERE TYPE == :type "

        query = "SELECT * FROM 'EVENTS' " + where_clause + "ORDER BY TIMESTAMP DESC LIMIT :limit OFFSET :offset"

        return Event.load_all_from_db(query, params, db)

    @staticmethod
    def get_unseen_events(user, db):
        last_checked = user.events_last_checked

        events = Event.load_all_from_db("SELECT * FROM 'EVENTS' WHERE TIMESTAMP > :time",
                        {'time': last_checked}, db)

        return len(events)

    @staticmethod
    def load_all_types_from_db(types, db=None):
        return Event.load_all_from_db('SELECT * FROM EVENTS WHERE TYPE IN (%s)' % ','.join('?'*len(types)),
                                     types, db)

    @staticmethod
    #ID is username
    def load_from_db(id, db=None):
        items = Event.load_all_ids_from_db([id], db)

        if ((len(items) == 0) or (items[0].id != id)):
            raise ItemNotFoundException("Could not find event-id: " + id)
        else:
            return items[0]

    @staticmethod
    def load_all(db=None):
        return Event.load_all_from_db('SELECT * FROM EVENTS', {}, db)

    @staticmethod
    def create_from_dict(dict):
        try:
            id = dict['id']
            timestamp = dict['timestamp']
            text = dict['text']
            type = dict['type']

            user = Event(text, type, timestamp, id)

            return user
        except:
            raise InvalidParametersException("Event.create_from_dict(): invalid dict")