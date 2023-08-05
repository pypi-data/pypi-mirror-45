from homevee.exceptions import InvalidParametersException, AbstractFunctionCallException


class Item():
    def __init__(self):
        pass

    def save_to_db(self, db=None):
        raise AbstractFunctionCallException("Item.save_to_db() is abstract")

    def build_dict(self):
        raise AbstractFunctionCallException("Item.build_dict() is abstract")

    def get_dict(self, fields=None):
        dict = self.build_dict()

        if (fields is None):
            return dict
        else:
            try:
                output_dict = {}

                for field in fields:
                    output_dict[field] = dict[field]

                return output_dict
            except:
                raise InvalidParametersException("InvalidParams given for get_dict()")

    @staticmethod
    def load_all_ids_from_db(ids, db=None):
        raise AbstractFunctionCallException("Item.load_all_ids_from_db() is abstract")

    @staticmethod
    def load_all_from_db(query, params, db=None):
        raise AbstractFunctionCallException("Item.load_all_from_db() is abstract")

    @staticmethod
    def load_from_db(id, db=None):
        raise AbstractFunctionCallException("Item.load_from_db() is abstract")

    @staticmethod
    def create_from_dict(dict):
        raise AbstractFunctionCallException("Item.create_from_dict() is abstract")

    @staticmethod
    def list_to_dict(list):
        data = []

        for item in list:
            data.append(item.get_dict())

        return data