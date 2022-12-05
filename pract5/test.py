import unittest
import pract_functions

distance_test = [[(0, 0), (2, 2), 2.828], [(2, 2), (4, 5), 3.606], [(4, 5), (10, 2), 6.708]]
move_wait_time = [[2.828, 0.14], [3.606, 0.18], [6.708, 0.34]]
move_speed = 20
angle_test = [[(1, 1), (2, 2), 0], [(2, 2), (4, 5), 6.34], [(4, 5), (10, 2), 40.03]]
angle_wait_time = [[0, 0], [6.34, 0.21], [40.03, 1.33]]
rot_speed = 30


class DistanceCalcTest(unittest.TestCase):
    def test_calc_distance(self):
        for i in range(len(distance_test)):
            result = pract_functions.calc_distance((distance_test[i])[0], (distance_test[i])[1])
            self.assertEqual(result, (distance_test[i])[2])

    def test_move_wait(self):
        for i in range(len(move_wait_time)):
            result = pract_functions.wait_move((move_wait_time[i])[0], move_speed)
            self.assertEqual(result, (move_wait_time[i])[1])

    def test_calc_angle(self):
        for i in range(len(angle_test)):
            result = pract_functions.calc_angle((angle_test[i])[0], (angle_test[i])[1])
            self.assertEqual(result, (angle_test[i])[2])

    def test_wait_angle(self):
        for i in range(len(angle_wait_time)):
            result = pract_functions.wait_rotation((angle_wait_time[i])[0], rot_speed)
            self.assertEqual(result, (angle_wait_time[i])[1])


test = DistanceCalcTest()
test.test_calc_distance()
test.test_move_wait()
test.test_calc_angle()
test.test_wait_angle()
