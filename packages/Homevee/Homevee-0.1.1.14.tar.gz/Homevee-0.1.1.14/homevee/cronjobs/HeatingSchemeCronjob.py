#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime

from homevee.DeviceAPI.heating import heating_control
from homevee.Helper import Logger
from homevee.cronjobs import IntervalCronjob
from homevee.utils.database import get_database_con


class HeatingSchemeCronjob(IntervalCronjob):
    def __init__(self):
        super(HeatingSchemeCronjob, self).__init__(task_name="HeatingScheme", interval_seconds=60)

    def task_to_do(self, *args):
        self.run_heating_scheme()

    def run_heating_scheme(self):
        db = get_database_con()

        current_datetime = datetime.datetime.now()

        with db:
            cur = db.cursor()

            #Query heating scheme for this day and time
            query = 'SELECT * FROM HEATING_SCHEME, HEATING_SCHEME_DAYS, HEATING_SCHEME_DEVICES WHERE HEATING_SCHEME.ID = HEATING_SCHEME_ID AND HEATING_SCHEME.ID = HEATING_SCHEME_DEVICES.ID AND ACTIVE = "true" AND TIME = :time AND WEEKDAY_ID = :day;'

            current_time = current_datetime.strftime("%H:%M")
            current_day = current_datetime.weekday()

            #Run command
            cur.execute(query, {'time': current_time, 'day': current_day})

            for item in cur.fetchall():
                Logger.log(item)

                heating_control(None, item['TYPE'], item['DEVICE_ID'], item['VALUE'], db, check_user=False)