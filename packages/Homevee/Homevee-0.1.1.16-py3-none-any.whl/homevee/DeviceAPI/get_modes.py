#!/usr/bin/python
# -*- coding: utf-8 -*-

from homevee.DeviceAPI.zwave.get_devices import get_device_value
from homevee.exceptions import NoSuchTypeException
from homevee.items.Device.Switch.Funksteckdose import Funksteckdose
from homevee.items.Room import Room
from homevee.items.Status import *
from homevee.utils.device_types import *

def get_mode(type, id, db):
    if type == FUNKSTECKDOSE:
        item = Funksteckdose.load_from_db(id)
    else:
        raise NoSuchTypeException("type "+type+" does not exist")

    return item.mode

def get_modes(user, room, type, id, db):
    if not user.has_permission(room):
        return Status(type=STATUS_NO_PERMISSION).get_dict()

    room = Room.load_from_db(room)

    if id is None or id == "":
        modi = []

        devices = {}

        #Funksteckdose
        devices[FUNKSTECKDOSE] = Funksteckdose.get_all(room, db)

        for device_type in devices:
            for device in devices[device_type]:
                item = device.get_dict()

                modi.append(item)

        return {'modi': modi}

    else:
        return get_mode(type, id, db)


    if id == "":
        modi = []

        with db:
            cur = db.cursor()

            #Funksteckdosen laden
            cur.execute("SELECT * FROM FUNKSTECKDOSEN WHERE ROOM == :room", {'room': room})
            for item in cur.fetchall():
                mode_item = {'device': item['DEVICE'], 'mode': item['ZUSTAND'], 'icon': item['ICON'],
                    'name': item['NAME'], 'type': FUNKSTECKDOSE}
                modi.append(mode_item)

            #Z-Wave Schalter
            cur.execute("SELECT * FROM ZWAVE_SWITCHES WHERE LOCATION == :room", {'room': room})
            for item in cur.fetchall():
                mode_item = {'device': item['ID'], 'mode': get_modes(username, room, "Z-Wave Schalter", item['ID'], db), 'icon': item['ICON'],
                             'name': item['NAME'], 'type': ZWAVE_SWITCH}
                modi.append(mode_item)

            cur.close()

            return {'modi': modi}
    else:
        with db:
            cur = db.cursor()

            if type == FUNKSTECKDOSE:
                cur.execute("SELECT * FROM FUNKSTECKDOSEN WHERE DEVICE == :device", {'device': id})
                return cur.fetchone()['ZUSTAND']
            elif type == ZWAVE_SWITCH:
                '''gateway_data = get_gateway("Z-Wave", db)

                port = ""

                if gateway_data['PORT'] is not None and gateway_data['PORT'] != "":
                    port = ":"+gateway_data['IP'];

                link = "http://"+gateway_data['IP']+port+"/ZAutomation/api/v1/devices/"+id

                result = "{}"

                array = json.loads(result)

                if "code" not in array or array['code'] != "200":
                    return "false"

                return str(array['data']['metrics']['level'] == "on")'''
                return get_device_value(ZWAVE_SWITCH, id, db)