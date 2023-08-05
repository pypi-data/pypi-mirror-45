#!/usr/bin/python
# -*- coding: utf-8 -*-

from homevee.items.Device.Sensor.ZWaveSensor import *
from homevee.items.Room import Room
from homevee.items.Status import *
from homevee.utils.device_types import *

SENSOR_TYPE_MAP = {
    'temp': {'name': 'Temperatur', 'einheit': '°C', 'einheit_word': 'Grad'},
    'hygro': {'name': 'Luftfeuchtigkeit', 'einheit': '%', 'einheit_word': '%'},
    'helligkeit': {'name': 'Helligkeit', 'einheit': 'Lux', 'einheit_word': 'Lumen'},
    'uv': {'name': 'UV-Licht', 'einheit': 'UV-Index', 'einheit_word': 'UV-Index'},
    'powermeter': {'name': 'Stromverbrauch', 'einheit': 'Watt', 'einheit_word': 'Watt'},
}


def get_einheit(type, id, db):
    with db:
        cur = db.cursor()
        db_data = {
            ZWAVE_SENSOR: {'table': 'ZWAVE_SENSOREN', 'sensor_type_col': 'SENSOR_TYPE', 'id_col': 'ID'},
            MQTT_SENSOR: {'table': 'MQTT_SENSORS', 'sensor_type_col': 'TYPE', 'id_col': 'ID'}
        }

        cur.execute("SELECT " + db_data[type]['sensor_type_col'] + " FROM " + db_data[type]['table'] + " WHERE " +
                    db_data[type]['id_col'] + " = :id",
                    {'id': id})

        return SENSOR_TYPE_MAP[cur.fetchone()[db_data[type]['sensor_type_col']]]['einheit']


def get_sensor_value(type, id, show_einheit, db):
    # TODO Klassen für Sensor-Typen erweitern

    if type == ZWAVE_SENSOR:
        sensor = ZWaveSensor.load_from_db(id, db)
    # elif type == ZWAVE_THERMOSTAT:
    #	sensor = ZWaveThermostat.load_from_db(id, db)
    # elif type == RADEMACHER_THERMOSTAT:
    #	sensor = RademacherThermostat.load_from_db(id, db)
    else:
        return "N/A"

    output = str(sensor.value)

    if show_einheit:
        output += " " + sensor.get_einheit()

    return output


def get_sensor_data(user, room, type, id, show_einheit, db):
    if not user.has_permission(room):
        return Status(type=STATUS_NO_PERMISSION).get_dict()

    values = []

    for room in Room.load_all(db):
        value_array = []

        if not user.has_permission(room.id):
            continue

        devices = {}

        # ZWave Sensoren
        devices[ZWAVE_THERMOSTAT] = ZWaveSensor.get_all(room, db)

        # TODO weitere Sensortypen

        # Iterate through all collected sensors

        for device_type in devices:
            for device in devices[device_type]:
                item = device.get_dict()
                value_array.append(item)

        value_item = {'name': room.name, 'location': room.id, 'icon': room.icon,
                      'value_array': value_array}

        values.append(value_item)

    return {'values': values}
