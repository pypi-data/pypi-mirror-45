from homevee.exceptions import ShoppingListItemNotFoundException, InvalidParametersException
from homevee.items import Item
from homevee.utils import database


class ShoppingListItem(Item):
    def __init__(self, item, amount, id=None):
        super(ShoppingListItem, self).__init__()

        self.id = id
        self.item = item
        self.amount = amount

    def delete(self, db=None):
        try:
            if (db is None):
                db = database.get_database_con()

            with db:
                cur = db.cursor()
                cur.execute("DELETE FROM SHOPPING_LIST WHERE ID == :id", {'id': self.id})
                return True
        except:
            return False

    def save_to_db(self, db=None):
        if (db is None):
            db = database.get_database_con()

        with db:
            cur = db.cursor()

            if(self.id is None or self.id == ""):
                #TODO Check if entry with same name exists and notify user(???)

                cur.execute("INSERT OR IGNORE INTO SHOPPING_LIST (AMOUNT, ITEM) VALUES (:amount, :name);",
                            {'amount': self.amount, 'name': self.name})
            else:
                cur.execute("UPDATE OR IGNORE SHOPPING_LIST SET AMOUNT = :amount, ITEM = :name WHERE ID = :id",
                            {'amount': self.amount, 'name': self.name, 'id': self.id})

    def get_dict(self, fields=None):
        dict = {
            'id': self.id,
            'item': self.item,
            'amount': self.amount
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
                raise InvalidParametersException("InvalidParams given for ShoppingListItem.get_dict()")

    @staticmethod
    def load_all_ids_from_db(ids, db=None):
        return ShoppingListItem.load_all_from_db('SELECT * FROM SHOPPING_LIST WHERE ID IN (%s)' % ','.join('?' * len(ids)),
                                     ids, db)

    @staticmethod
    def load_all_from_db(query, params, db=None):
        items = []

        with db:
            cur = db.cursor()
            cur.execute(query, params)

            for item in cur.fetchall():
                if item['AMOUNT'] is None:
                    amount = -1
                else:
                    amount = int(item['AMOUNT'])

                items.append(ShoppingListItem(item['ITEM'], amount, item['ID']))

            cur.close()

        return items

    @staticmethod
    def load_all(db=None):
        return ShoppingListItem.load_all_from_db('SELECT * FROM SHOPPING_LIST', {}, db)

    @staticmethod
    def load_from_db(id, db=None):
        items = ShoppingListItem.load_all_ids_from_db([id], db)

        if ((len(items) == 0) or (str(items[0].id) != str(id))):
            raise ShoppingListItemNotFoundException("Could not find shopping-list-item with id: " + id)
        else:
            return items[0]

    @staticmethod
    def create_from_dict(dict):
        id = dict['id']
        item = dict['item']
        amount = dict['amount']

        return ShoppingListItem(item, amount, id)