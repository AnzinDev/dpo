import math

timescale = 1


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
