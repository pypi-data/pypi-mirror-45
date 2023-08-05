import os
import traceback

from passlib.handlers.pbkdf2 import pbkdf2_sha512

from homevee.exceptions import UserNotFoundException, InvalidParametersException, DatabaseSaveFailedException
from homevee.items import Item
from homevee.items.User.Permission import Permission
from homevee.utils import database


class User(Item):
    def __init__(self, username, hashed_password, ip, at_home, events_last_checked,
                 permissions, dashboard_data, salt, fcm_token, current_location, id=None):
        super(User, self).__init__()

        self.id = id
        self.username = username
        self.hashed_password = hashed_password
        self.ip = ip
        self.at_home = at_home
        self.events_last_checked = events_last_checked
        self.permissions = permissions
        self.dashboard_data = dashboard_data
        self.salt = salt
        self.fcm_token = fcm_token
        self.current_location = current_location

    def delete(self, db=None):
        pass

    def has_permission(self, permission):
        for user_permission in self.permissions:
            if user_permission.key == "admin" or user_permission.id == permission:
                return True

        return False

    @staticmethod
    def hash_password(password):
        salt = os.urandom(12).hex()

        hashed_pw = pbkdf2_sha512.encrypt(password + salt, rounds=200000)

        # print "Password: "+password
        # print "Salt: "+salt
        # print "Hashed: "+hashed_pw

        #self.hashed_password = hashed_pw
        #self.salt = salt

        return (hashed_pw, salt)

    def verify(self, password):
        try:
            return pbkdf2_sha512.verify(password + self.salt, self.hashed_password)
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
                    cur.execute("""INSERT INTO USERDATA (USERNAME, PASSWORD, IP, PERMISSIONS, PW_SALT) VALUES 
                                (:username, :password, :ip, :permissions, :salt)""",
                                {'username': self.username, 'password': self.hashed_password, 'ip': self.ip,
                                 'permissions': Permission.get_json_list(self.permissions), 'salt': self.salt})
                # update
                else:
                    cur.execute("""UPDATE USERDATA SET PASSWORD = :password, IP = :ip, PERMISSIONS = :permissions,
                                PW_SALT = :salt WHERE ID = :id""",
                                {'password': self.hashed_password, 'ip': self.ip,
                                 'permissions': Permission.get_json_list(self.permissions),
                                 'salt': self.salt, 'id': self.id})

                #TODO add generated id to object
        except:
            traceback.print_exc()
            raise DatabaseSaveFailedException("Could not save user to database")

    def get_dict(self, fields=None):
        dict = {
            'id': self.id,
            'username': self.username,
            'password': self.hashed_password,
            'ip': self.ip,
            'at_home': self.at_home,
            'events_last_checked': self.events_last_checked,
            'permissions': Permission.list_to_dict(self.permissions),
            'dashboard_data': self.dashboard_data,
            'salt': self.salt,
            'fcm_token': self.fcm_token,
            'current_location': self.current_location
        }

        if (fields is None):
            return dict
        else:
            try:
                output_dict = {}

                for field in fields:
                    output_dict[field] = dict[field]

                return output_dict
            except:
                raise InvalidParametersException("InvalidParams given for User.get_dict()")

    @staticmethod
    def load_all_from_db(query, params, db=None):
        if (db is None):
            db = database.get_database_con()

        users = []

        with db:
            cur = db.cursor()

            cur.execute(query, params)
            for result in cur.fetchall():
                user = User(result['USERNAME'], result['PASSWORD'], result['IP'], result['AT_HOME'],
                            result['EVENTS_LAST_CHECKED'], Permission.create_list_from_json(result['PERMISSIONS']),
                            result['DASHBOARD_DATA'], result['PW_SALT'], result['FCM_TOKEN'],
                            result['CURRENT_LOCATION'], result['ID'])
                users.append(user)

        return users

    @staticmethod
    def load_by_permission(permission, db=None):
        users = User.load_all(db)

        output = []

        for user in users:
            if user.has_permission(permission):
                output.append(user)

        return users

    @staticmethod
    def load_all_ids_from_db(ids, db=None):
        return User.load_all_from_db('SELECT * FROM USERDATA WHERE ID IN (%s)' % ','.join('?'*len(ids)),
                                     ids, db)

    @staticmethod
    def load_all_usernames_from_db(usernames, db=None):
        return User.load_all_from_db('SELECT * FROM USERDATA WHERE USERNAME IN (%s)' % ','.join('?'*len(usernames)),
                                     usernames, db)

    @staticmethod
    #ID is username
    def load_from_db(id, db=None):
        users = User.load_all_ids_from_db([id], db)

        if((len(users) == 0) or (users[0].id != id)):
            raise UserNotFoundException("Could not find user-id: "+id)
        else:
            return users[0]

    @staticmethod
    def load_all(db=None):
        return User.load_all_from_db('SELECT * FROM USERDATA', {}, db)

    @staticmethod
    #ID is username
    def load_username_from_db(username, db=None):
        users = User.load_all_usernames_from_db([username], db)

        if((len(users) == 0) or (users[0].username != username)):
            raise UserNotFoundException("Could not find username: "+username)
        else:
            return users[0]

    @staticmethod
    def create_from_dict(dict):
        try:
            id = dict['id']
            username = dict['username']
            password = dict['password']
            ip = dict['ip']
            at_home = dict['at_home']
            events_last_checked = dict['events_last_checked']
            permissions = Permission.list_from_dict(dict['permissions'])
            dashboard_data = dict['dashboard_data']
            salt = dict['salt']
            fcm_token = dict['fcm_token']
            current_location = dict['current_location']

            user = User(username, password, ip, at_home, events_last_checked,
                        permissions, dashboard_data, salt, fcm_token, current_location, id)

            return user
        except:
            raise InvalidParametersException("User.create_from_dict(): invalid dict")