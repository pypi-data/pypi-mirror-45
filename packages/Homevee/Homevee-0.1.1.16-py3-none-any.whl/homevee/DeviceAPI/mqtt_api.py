#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import socket
import time
import traceback
from time import sleep

import paho.mqtt.client as mqtt

from homevee.DeviceAPI.mqtt_sensor import handle_mqtt_sensor
from homevee.Helper import Logger, smarthome_functions, translations
from homevee.items.Gateway import *
from homevee.utils.database import get_database_con

MQTT_CLIENT = None

topics_to_subscribe = [
    '/home/#'
]

QUALITY_OF_SERVICE = 0

# https://www.dinotools.de/2015/04/12/mqtt-mit-python-nutzen/

def run_device_action(topic, msg, db):
    topic_parts = topic.split("/")

    #topic_parts[0] is empty
    #topic_parts[1] is "home"

    result = None

    if(topic_parts[2] == "device"):
        with db:
            cur = db.cursor()

            cur.execute("SELECT * FROM MQTT_DEVICES WHERE TOPIC = :topic",
                        {'topic': topic})

            result = cur.fetchone()

            key = result['KEY']

            # aes = AESCipher.AESCipher(key)
            # msg = aes.decrypt(msg)

            with db:
                cur = db.cursor()

                data = json.loads(msg)

                device_types = ["MQTT_SENSORS"]  # , "MQTT_TRIGGERS"]

                for device_type in device_types:
                    cur.execute("SELECT * FROM " + device_type + " WHERE DEVICE_ID = :dev_id",
                                {'dev_id': result['ID']})

                    result = cur.fetchall()

                    for device in result:
                        for data_item in data:
                            if str(device['VALUE_ID']) == str(data_item['id']):
                                handle_mqtt_sensor(device['ID'], data_item['value'], db)

                # Run MQTT-Trigger
                '''cur.execute("SELECT * FROM MQTT_TRIGGERS WHERE TOPIC = :topic", {'topic': message.topic})
                for item in cur.fetchall():
                    #handle item action
                    data = json.loads(msg)
                    Logger.log(data)
                    Logger.log(item)
                    run_trigger_automation("MQTT-Trigger", item['TYPE'], item['ID'], data['action'], db)
                    break'''
    elif(topic_parts[2] == "assistant" and topic_parts[4]=="send"):
        start_time = time.time()

        with db:
            cur = db.cursor()

            cur.execute("SELECT * FROM SMART_SPEAKER WHERE ID = :id",
                        {'id': topic_parts[3]})

            smart_speaker = cur.fetchone()

            topic = '/' + topic_parts[1] + '/' + topic_parts[2] + '/' + topic_parts[3] + '/receive'

            try:
                data = json.loads(msg)

                data = json.loads(data['msg'])

                username = data['username']
                text = data['text']

                text = text.encode('utf-8')

                result = smarthome_functions.do_voice_command(username, text, None, smart_speaker['LOCATION'], db, translations.LANGUAGE)

                result['time'] = time.time()
            except:
                if(Logger.IS_DEBUG):
                    traceback.print_exc()
                answer = "Es gab einen Fehler."
                result = {'msg_text': answer, 'msg_speech': answer}

            end_time = time.time()
            result['computing_duration'] = end_time - start_time

            publish(topic, json.dumps(result))

def publish(topic, msg):
    client = mqtt.Client()

    gateway = Gateway.load_from_db(MQTT_BROKER, get_database_con())

    Logger.log("publishing to "+topic+": "+msg)

    client.connect(gateway.ip)
    client.publish(topic, msg, QUALITY_OF_SERVICE, False)

def on_message(client, userdata, message):
    db = get_database_con()

    msg = str(message.payload.decode("utf-8"))
    Logger.log("message received: ", msg)
    Logger.log("message topic: ", message.topic)
    # Logger.log("message qos=",message.qos)
    # Logger.log("message retain flag=",message.retain)

    # decrypt message with saved key of the device in db
    try:
        run_device_action(message.topic, msg, db)
    except:
        if(Logger.IS_DEBUG):
                traceback.print_exc()

def on_connect(client, userdata, flags, rc):
    for topic in topics_to_subscribe:
        client.subscribe(topic, QUALITY_OF_SERVICE)

    for topic in get_topics():
        client.subscribe(topic, QUALITY_OF_SERVICE)


def init_client():
    while (True):
        gateway = Gateway.load_from_db(MQTT_BROKER, get_database_con())

        if gateway is None:
            sleep(30)

        try:
            broker_address = gateway.ip
        except:
            broker_address = None

        #keep retrying when broker_address is None
        if broker_address is None:
            sleep(15)
            continue

        try:
            client = mqtt.Client()
            client.on_connect = on_connect
            client.on_message = on_message

            client.connect(broker_address)

            Logger.log("Connected to MQTT Broker: " + broker_address)


            while(True):
                #check if client still connected and exit if not
                client.loop(1)

        except socket.error as e:
            continue
        # Logger.log("Cannot reach MQTT Broker: " + broker_address)


def get_topics():
    # load topics from database

    return []
