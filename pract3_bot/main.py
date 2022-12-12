import pygame
import math
import constants as c
from paho.mqtt import client as mqtt

timescale = 1
broker = "localhost"
port = 1883
topic = "house/topic1"
msg_count = 0
read_data = []
dist = 0
angle = 0

def main():
    client = mqtt.Client("mqtt-sub-1")
    client.connect(broker, port)

    def on_message(client, userdata, message):
        points = list(message.payload.decode())
        dist = calc_distance(points[0], points[1])
        angle = calc_angle(points[0], points[1])

    client.on_message = on_message
    client.on_message
    client.subscribe(topic)
    client.loop_forever()
    pygame.init()
    screen = pygame.display.set_mode((c.WIDTH, c.HEIGHT))
    pygame.display.set_caption("ABOT")
    clock = pygame.time.Clock()
    running = True
    bot = pygame.rect.Rect(height=5, width=5)
    while running:
        clock.tick(c.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(c.WHITE)
        move_bot(bot, angle, dist)
        pygame.display.flip()
    pygame.quit()


def calc_distance(p_from, p_to):
    return round(math.sqrt((p_from[0] - p_to[0]) * (p_from[0] - p_to[0]) + (p_from[1] - p_to[1]) * (p_from[1] - p_to[1])), 3)


def calc_angle(p_from, p_to):
    return round(math.degrees(math.acos((p_from[0] * p_to[0] + p_from[1] * p_to[1]) / (
                math.sqrt(p_to[0] ** 2 + p_to[1] ** 2) * math.sqrt(p_from[0] ** 2 + p_from[1] ** 2)))), 3)


def wait_rotation(angle, rot_speed):
    waiting_time = round(timescale * (angle / rot_speed), 2)
    print(f"Wait rotation for: {waiting_time} seconds.")
    return waiting_time


def wait_move(dist, speed):
    waiting_time = round(timescale * (dist / speed), 2)
    print(f"Wait movement for: {waiting_time} seconds.")
    return waiting_time


if __name__ == '__main__':
    main()


