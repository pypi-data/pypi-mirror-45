#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

import requests

from homevee.Helper import Logger
from homevee.items.Gateway import Gateway
from homevee.utils.database import get_database_con


def get_rooms():
    result = {}

    gateway = Gateway.load_from_db('Z-Wave', get_database_con())

    port = ""
    if (gateway.port != None and gateway.port != ""):
        port = ":" + str(gateway.port)

    url = "http://" + gateway.key1 + ':' + gateway.key2 + '@' + gateway.ip\
          + port + "/ZAutomation/api/v1/locations/"
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    request = requests.get(url, headers=headers)
    data = request.content

    Logger.log(data)

    result = json.loads(data)

    return result