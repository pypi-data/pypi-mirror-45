#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import urllib.error
import urllib.parse
import urllib.request

from homevee.items.Gateway import *


def get_devices(db):
    gateway = Gateway.load_from_db(RADEMACHER_HOMEPILOT, db)

    devices = []

    url = "http://"+gateway.ip+"/deviceajax.do?devices=1"

    response = urllib.request.urlopen(url).read()

    data = json.loads(response)

    for device in data['devices']:
        item = {'title': device['name'], 'id': device['did'], 'info': device['description']}

        devices.append(item)

    return {'devices': devices}