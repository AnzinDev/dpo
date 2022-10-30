from ast import For
from random import random
from paho.mqtt import client as mqtt
import time

broker = "localhost"
port = 1883
topic = "house/topic1"
file_path = "data.txt"

def main():
    client = mqtt.Client(f"mqtt-pub-8")
    broker_connect(client)
    with open(file_path) as f:
        lines = f.readlines()
        lines.pop()
        for num in lines:
            pub(client, num[:- 1])
            time.sleep(1)
    disconnect(client)


def broker_connect(client):
    client.connect(broker, port)


def pub(client, message):
    result = client.publish(topic, message)
    if result[0] == 0:
        print(f"Sent message: {message} to topic: {topic}")
    else:
        print("Error")


def disconnect(client):
    client.disconnect()


main()
