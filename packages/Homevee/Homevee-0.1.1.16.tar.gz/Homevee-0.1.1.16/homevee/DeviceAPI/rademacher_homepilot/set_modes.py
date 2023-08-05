#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib.error
import urllib.parse
import urllib.request

from homevee.items.Gateway import *


def set_modes(id, mode, db):
    gateway = Gateway.load_from_db(RADEMACHER_HOMEPILOT, db)

    url = "http://" + gateway.ip + "/deviceajax.do?cid=9&did=10001&goto=" + str(mode) + "&command=0"

    response = urllib.request.urlopen(url).read()