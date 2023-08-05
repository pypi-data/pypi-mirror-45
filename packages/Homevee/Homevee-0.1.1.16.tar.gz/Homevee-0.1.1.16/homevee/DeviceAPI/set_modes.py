#!/usr/bin/python
# -*- coding: utf-8 -*-
import traceback
import urllib.error
import urllib.parse
import urllib.request

from homevee.DeviceAPI import zwave
from homevee.Helper import Logger
from homevee.Helper.helper_functions import has_permission
from homevee.items.Device.Switch.Funksteckdose import Funksteckdose
from homevee.items.Status import *
from homevee.utils.device_types import *


def set_modes(username, type, id, mode, db, check_user=True):
    if type == FUNKSTECKDOSE:
        return set_socket(username, id, mode, db, check_user)
    elif type == ZWAVE_SWITCH:
        return set_zwave_switch(username, id, mode, db, check_user)
    elif type == URL_SWITCH:
        return set_url_switch_binary(username, id, mode, db, check_user)
    elif type == URL_TOGGLE:
        return set_url_toggle(username, id, db, check_user)
    else:
        raise ValueError("Type does not exist")

def set_url_switch_binary(username, id, mode, db, check_user=True):
    with db:
        cur = db.cursor()
        cur.execute("SELECT * FROM URL_SWITCH_BINARY WHERE ID == :id",
                    {'id': id})

        data = cur.fetchone()

        if check_user and not has_permission(username, data['LOCATION'], db):
            return {'result': 'nopermission'}

        if mode == "":
            urllib.request.urlopen(data['URL_ON'])
        else:
            urllib.request.urlopen(data['URL_OFF'])

    return Status(type=STATUS_OK).get_dict()

def set_url_toggle(username, id, db, check_user=True):
    with db:
        cur = db.cursor()
        cur.execute("SELECT * FROM URL_TOGGLE WHERE ID == :id",
                    {'id': id})

        data = cur.fetchone()

        if check_user and not has_permission(username, data['LOCATION'], db):
            return {'result': 'nopermission'}

        urllib.request.urlopen(data['TOGGLE_URL'])

    return Status(type=STATUS_OK).get_dict()

def set_socket(user, id, mode, db, check_user=True):
    try:
        funksteckdose = Funksteckdose.load_from_db(id, db)

        if check_user and not user.has_permission(funksteckdose.location):
            return {'result': 'nopermission'}

        if(funksteckdose.set_mode(mode, db)):
            return Status(type=STATUS_OK).get_dict()
    except:
        if(Logger.IS_DEBUG):
                traceback.print_exc()
    return Status(type=STATUS_ERROR).get_dict()

def set_zwave_switch(username, id, mode, db, check_user=True):
    try:
        with db:
            cur = db.cursor()
            cur.execute("SELECT * FROM ZWAVE_SWITCHES WHERE ID == :device",
                        {'device': id})

            data = cur.fetchone()

            if check_user and not has_permission(username, data['LOCATION'], db):
                return {'result': 'nopermission'}

            device_id = data['ID']

            state = "on" if (int(mode) == 1) else "off"

            result = zwave.device_control.set_binary_device(device_id, state, db)

            if result['code'] == 200:
                cur.execute("UPDATE ZWAVE_SWITCHES SET VALUE = :value WHERE ID = :id",
                            {'value': mode, 'id': id})

                return Status(type=STATUS_OK).get_dict()
    except Exception as e:
        if Logger.IS_DEBUG:
            if(Logger.IS_DEBUG):
                traceback.print_exc()
        return Status(type=STATUS_ERROR).get_dict()

def set_diy_switch(id, mode, db, check_user=True):
    return