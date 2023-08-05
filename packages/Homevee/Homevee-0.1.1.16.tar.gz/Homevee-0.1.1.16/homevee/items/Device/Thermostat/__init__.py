from homevee.exceptions import AbstractFunctionCallException
from homevee.items.Device import Device


class Thermostat(Device):
    def __init__(self, name, icon, location, id=None, temp=None):
        super(Thermostat, self).__init__(name, icon, location, id=id)
        self.temp = temp

    def set_temp(self, temp, db=None):
        if(self.update_temp(temp, db)):
            self.mode = temp
            self.save_to_db(db)
            print("result == True")
            return True
        print("result == False")
        return False

    def update_temp(self, temp, db=None):
        raise AbstractFunctionCallException("Switch.update_mode() is abstract")

    #@staticmethod
    #def get_all(location=None, db=None):
    #    # get all devices of all types
    #    devices = []
    #    devices.extend(Switch.get_all(location, db))
    #    return devices