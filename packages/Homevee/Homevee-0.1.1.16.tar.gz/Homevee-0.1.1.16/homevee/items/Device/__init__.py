from homevee.exceptions import AbstractFunctionCallException, InvalidParametersException
from homevee.items import Item


class Device(Item):
    def __init__(self, name, icon, location, id=None):
        super(Device, self).__init__()

        self.id = id
        self.name = name
        self.icon = icon
        self.location = location

    def get_device_type(self):
        raise AbstractFunctionCallException("Device.get_device_type() is abstract")

    def get_dict(self, fields=None):
        output_dict = {}

        dict = self.build_dict()

        if (fields is None):
            output_dict = dict
        else:
            try:
                for field in fields:
                    output_dict[field] = dict[field]
            except:
                raise InvalidParametersException("InvalidParams given for get_dict()")

        output_dict['device_type'] = self.get_device_type()

        return output_dict