#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime

from homevee.Functions.Automations import Automation
from homevee.cronjobs import IntervalCronjob
from homevee.utils.database import get_database_con


class TimedAutomationsCronjob(IntervalCronjob, Automation):
    def __init__(self):
        super(TimedAutomationsCronjob, self).__init__(task_name="TimedAutomationsCronjob", interval_seconds=60)

    def task_to_do(self, *args):
        self.run_timed_automations()

    def run_timed_automations(self):
        # print "running automations"
        db = get_database_con()
        with db:
            cur = db.cursor()

            today = datetime.datetime.today()

            hour = today.hour
            minute = today.minute

            hour_string = str(hour)
            if (hour < 10):
                hour_string = "0" + hour_string

            minute_string = str(minute)
            if (minute < 10):
                minute_string = "0" + minute_string

            time_string = hour_string + ":" + minute_string

            # print time_string

            cur.execute(
                'SELECT * FROM AUTOMATION_DATA, AUTOMATION_TRIGGER_DATA WHERE AUTOMATION_DATA.ID = AUTOMATION_RULE_ID AND TYPE = "time" AND IS_ACTIVE = "true" AND VALUE = :val',
                {'val': time_string})

            automations = cur.fetchall()

            self.run_automations(automations, db)

        return