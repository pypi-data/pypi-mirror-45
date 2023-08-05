class UserNotFoundException(Exception):
    '''Raised when a user was not found'''
    pass

class RoomNotFoundException(Exception):
    '''Raised when a room was not found'''
    pass

class ShoppingListItemNotFoundException(Exception):
    '''Raised when a room was not found'''
    pass

class InvalidParametersException(Exception):
    '''Raised when parameters where invalid'''
    pass

class DatabaseSaveFailedException(Exception):
    '''Raised when saving to database fails'''
    pass