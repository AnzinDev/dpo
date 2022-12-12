from paho.mqtt import client as mqtt
import time
import math


broker = "localhost"
port = 1883
topic = "topic1"
file_path = "data.txt"
points = []


class publisher():
    def start(self, path):
        client = mqtt.Client(f"mqtt-pub-1")
        broker_connect(client)
        points_list = []
        with open(path) as f:
            points_list = f.readlines()
        for point in points_list:
            coords = point[:-1].split(' ')
            points.append((float(coords[0]), float(coords[1])))
            pub(client, points[:- 1])
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

