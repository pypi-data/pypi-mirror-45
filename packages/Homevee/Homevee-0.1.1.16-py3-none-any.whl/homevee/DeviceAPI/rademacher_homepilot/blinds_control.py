#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import urllib.error
import urllib.parse
import urllib.request
from homevee.items.Status import *
from homevee.Helper import Logger
from homevee.items.Gateway import *


def control_blinds(id, goto, db):
    gateway = Gateway.load_from_db(RADEMACHER_HOMEPILOT, db)

    url = "http://"+gateway.ip+"/deviceajax.do?cid=9&did="+str(id)+"&goto="+str(goto)+"&command=0"

    Logger.log(url)

    response = urllib.request.urlopen(url).read()

    data = json.loads(response)

    if(data['status'] != 'uisuccess'):
        return Status(type=STATUS_ERROR).get_dict()

    Logger.log(response)

    with db:
        cur = db.cursor()

        cur.execute("UPDATE HOMEPILOT_BLIND_CONTROL SET LAST_POS = :pos WHERE ID == :id",
                    {'pos': goto, 'id': id})
    return Status(type=STATUS_OK).get_dict()