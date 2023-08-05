import json

from homevee.exceptions import InvalidParametersException
from homevee.items.Room import Room


class Permission():
    def __init__(self, permission_key, name=None):
        if name is not None:
            self.name = name
        else:
            if permission_key == "admin":
                self.name = "Administrator"
            else:
                self.name = Room.get_name_by_id(permission_key, None)

        self.key = permission_key

    def get_dict(self, fields=None):
        dict = {
            'key': self.key,
            'name': self.name
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
                raise InvalidParametersException("InvalidParams given for Permission.get_dict()")

    @staticmethod
    def create_list_from_json(json_string):
        data = json.loads(json_string)

        permissions = []

        for item in data['permissions']:
            permissions.append(Permission(item))

        return permissions

    @staticmethod
    def list_to_dict(list):
        permissions = []

        for item in list:
            permissions.append(item.get_dict())

        return permissions

    @staticmethod
    def list_from_dict(dict):
        permissions = []

        for item in dict:
            permissions.append(Permission(item['key'], item['name']))

        return permissions


    @staticmethod
    def get_json_list(permissions):
        data = []

        for permission in permissions:
            data.append(permission.key)

        permission_data = {'permissions': data}

        return json.dumps(permission_data)