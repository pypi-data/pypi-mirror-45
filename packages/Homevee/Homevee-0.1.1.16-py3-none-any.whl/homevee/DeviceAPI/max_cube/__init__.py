#!/usr/bin/python
# -*- coding: utf-8 -*-

from pymax.cube import Cube

from homevee.Helper import Logger
from homevee.items.Gateway import Gateway
from homevee.items.Status import *


def get_devices(ip):
    thermostats = []
    try:
        with Cube(ip) as cube:
            for room in cube.rooms:
                for device in room.devices:
                    Logger.log(device)
                    thermostat = {'title': device.name, 'id': device.serial, 'room': room.name}

                    thermostats.append(thermostat)
    except:
        thermostats = []

    return thermostats


def set_temp(id, value, db):
    gateway = Gateway.load_from_db("MAX! Cube", db)

    try:
        with Cube(gateway.ip) as cube:
            for room in cube.rooms:
                for device in room.devices:
                    if id == device.serial:
                        result = cube.set_mode_manual(room.room_id, room.rf_address, float(value))

                        Logger.log(result)

                        with db:
                            cur = db.cursor()

                            cur.execute("UPDATE MAX_THERMOSTATS SET LAST_TEMP = :temp WHERE ID == :id",
                                        {'temp': value, 'id': id})

                        return Status(type=STATUS_OK).get_dict()
    except:
        return Status(type=STATUS_ERROR).get_dict()