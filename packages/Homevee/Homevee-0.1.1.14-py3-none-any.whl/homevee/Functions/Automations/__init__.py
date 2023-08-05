#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from homevee.Functions.condition_actions.actions import run_actions
from homevee.Functions.condition_actions.conditions import conditions_true
from homevee.Helper import Logger

class Automation():
    def run_trigger_automation(self, trigger_type, type, id, value, db):
        return

    def run_automations(self, automations, db):
        for item in automations:
            Logger.log(item)
            if (conditions_true(json.loads(item['CONDITION_DATA']), db)):
                if (int(item['TRIGGERED']) == 0):
                    Logger.log("running item: "+str(item))
                    run_actions(json.loads(item['ACTION_DATA']), db)
                    self.set_triggered(item['ID'], 1, db)
            else:
                self.set_triggered(item['ID'], 0, db)

    def set_triggered(self, id, triggered, db):
        with db:
            cur = db.cursor()

            cur.execute("UPDATE AUTOMATION_DATA SET TRIGGERED = :triggered WHERE ID = :id",
                        {'triggered': triggered, 'id': id})