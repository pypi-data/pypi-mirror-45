class Item():
    def __init__(self):
        pass

    def save_to_db(self, db=None):
        pass

    def get_dict(self, fields=None):
        return {}

    @staticmethod
    def load_all_ids_from_db(ids, db=None):
        pass

    @staticmethod
    def load_all_from_db(query, params, db=None):
        pass

    @staticmethod
    def load_from_db(id, db=None):
        pass

    @staticmethod
    def create_from_dict(dict):
        pass

    @staticmethod
    def list_to_dict(list):
        data = []

        for item in list:
            data.append(item.get_dict())

        return data