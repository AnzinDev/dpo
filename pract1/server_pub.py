from paho.mqtt import client as mqtt
import sys
import math
import time

timescale = 1

class publisher:
    def __init__(self, brocker_adr, port, topic, spd, ang) -> None:
        self.client = mqtt.Client('Server')
        def on_connect():
            print(f'Connected to brocker: {self.brk_adr}')
        self.client.on_connect = on_connect
        def on_connect_failure():
            print(f'Connection failure')
        self.client.on_connect_fail = on_connect_failure
        self.client.connect(brocker_adr, port)
        self.topic = topic
        if spd <= 0:
            self.speed = 1
            print('Zero speed is prohibited. Changed to 1.')
        else:
            self.speed = spd
        if ang <= 0:
            self.rotation_speed = 1
            print('Zero rotation speed is prohibited. Changed to 1.')
        else:
            self.rotation_speed = ang

    def publish(self, msg) -> None:
        res = self.client.publish(payload=msg, topic=self.topic)
        if res[0] == 0:
            print(f'Published: {msg} to topic: {self.topic}')
        else:
            print('Publish failure')

points = []

def read_point_file(path):
    points_list = []
    with open(path) as f:
        points_list = f.readlines()
    for point in points_list:
        coords = point[:-1].split(' ')
        points.append((float(coords[0]), float(coords[1])))


def algotithm_exec(client):
    base_angle = 0
    for i in range(len(points) - 1):
        curr = points[i]
        next = points[i + 1]
        if i == 0:
            distance = math.sqrt((next[0]) * (next[0]) + (next[1]) * (next[1]))
            angle = math.degrees(math.acos((0 * next[0] + 1 * next[1]) / (math.sqrt(next[0] * next[0] + next[1] * next[1]))))
            client.publish(f"{{\"cmd\":rotation, \"value\":\"{round(angle, 2)}\"}}")
            wait_rotation(angle, client.rotation_speed)
            client.publish(f"{{\"cmd\":movement, \"value\":\"{round(distance, 2)}\"}}")
            wait_move(distance, client.speed)
            continue
        distance = CalcDistanse(curr, next)
        angle = CaclAngle(curr, next)
        client.publish(f"{{\"cmd\":rotation, \"value\":\"{round(angle, 2)}\"}}")
        wait_rotation(angle, client.rotation_speed)
        client.publish(f"{{\"cmd\":movement, \"value\":\"{round(distance, 2)}\"}}")
        wait_move(distance, client.speed)


def CalcDistanse(p_from, p_to):
    return math.sqrt((p_from[0] - p_to[0]) * (p_from[0] - p_to[0]) + (p_from[1] - p_to[1]) * (p_from[1] - p_to[1]))


def CaclAngle(p_from, p_to):
    return math.degrees(math.acos((p_from[0] * p_to[0] + p_from[1] * p_to[1]) / (math.sqrt(p_to[0] ** 2 + p_to[1] ** 2) * math.sqrt(p_from[0] **2  + p_from[1] ** 2))))


def wait_rotation(angle, rot_speed):
    waiting_time = round(timescale * (angle / rot_speed))
    print(f"Wait rotation for: {waiting_time} seconds.")
    time.sleep(waiting_time)


def wait_move(dist, speed):
    waiting_time = round(timescale * (dist / speed), 2)
    print(f"Wait movement for: {waiting_time} seconds.")
    time.sleep(waiting_time)


def main():
    read_point_file(f'./{sys.argv[6]}')
    client = publisher(brocker_adr=sys.argv[1], port=int(sys.argv[2]), topic=sys.argv[3], spd=float(sys.argv[4]), ang=float(sys.argv[5]))
    algotithm_exec(client)

main()