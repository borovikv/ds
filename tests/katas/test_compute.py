from unittest import TestCase

import katas.self_driving_rides as subj


# input_file = [
#     [3, 4, 2, 3, 2, 10],
#     [0, 0, 1, 3, 2, 9],
#     [1, 2, 1, 0, 0, 9],
#     [2, 0, 2, 2, 0, 9],
# ]


class TestCompute(TestCase):
    def test_one_ride(self):
        map = subj.Map(rows=1, columns=2, vehicles=1, rides=1, bonus=1, steps=1)
        rides = [subj.Ride(id=0, start_x=0, start_y=0, end_x=1, end_y=0, earliest_start=0, latest_finish=1)]

        result = subj.compute(map, rides)
        expected = {1: [0]}
        self.assertEqual(result, expected)

    def test_two_rides_with_one_suitable(self):
        map = subj.Map(rows=1, columns=3, vehicles=1, rides=1, bonus=1, steps=1)
        rides = [
            subj.Ride(id=0, start_x=1, start_y=0, end_x=0, end_y=0, earliest_start=0, latest_finish=1),
            subj.Ride(id=1, start_x=0, start_y=0, end_x=1, end_y=0, earliest_start=0, latest_finish=1)
        ]

        result = subj.compute(map, rides)
        expected = {1: [1]}
        # todo: check
        print('abc', result)
        self.assertEqual(result, expected)

    def test_two_rides(self):
        map = subj.Map(rows=1, columns=3, vehicles=1, rides=1, bonus=1, steps=2)
        rides = [
            subj.Ride(id=0, start_x=1, start_y=0, end_x=0, end_y=0, earliest_start=0, latest_finish=1),
            subj.Ride(id=1, start_x=0, start_y=0, end_x=1, end_y=0, earliest_start=0, latest_finish=1)
        ]

        result = subj.compute(map, rides)
        expected = {1: [1, 0]}
        self.assertEqual(result, expected)

    def test_two_rides_two_cars(self):
        map = subj.Map(rows=1, columns=3, vehicles=2, rides=1, bonus=1, steps=1)
        rides = [
            subj.Ride(id=0, start_x=0, start_y=0, end_x=1, end_y=0, earliest_start=0, latest_finish=1),
            subj.Ride(id=1, start_x=0, start_y=0, end_x=1, end_y=0, earliest_start=0, latest_finish=1)
        ]

        result = subj.compute(map, rides)
        expected = {
            1: [0],
            2: [1],
        }
        # self.assertTrue(False)
        # self.assertEqual(result, expected)
        # self.assertEqual(sorted(result.values()), sorted(expected.values()))


    def _test_one_ride_with_offset(self):
        map = subj.Map(rows=1, columns=2, vehicles=1, rides=1, bonus=1, steps=2)
        rides = [
            subj.Ride(id=0, start_x=1, start_y=0, end_x=0, end_y=0, earliest_start=0, latest_finish=2),
            subj.Ride(id=1, start_x=1, start_y=0, end_x=0, end_y=0, earliest_start=0, latest_finish=2)
        ]

        result = subj.compute(map, rides)
        expected = {1: [0]}
        self.assertEqual(result, expected)

    def test_find_closest_vehicle(self):
        ride = subj.Ride(id=0, start_x=1, start_y=0, end_x=0, end_y=0, earliest_start=0, latest_finish=2)
        v1 = subj.Vehicle(1, subj.Point(0, 0))
        v2 = subj.Vehicle(2, subj.Point(1, 0))

        self.assertEqual(subj.find_closest_vehicle(ride, time=0, vehicles=[v1, v2]), v2)

    def test_find_closest_free_vehicle(self):
        ride = subj.Ride(id=0, start_x=1, start_y=0, end_x=0, end_y=0, earliest_start=0, latest_finish=2)
        v1 = subj.Vehicle(1, subj.Point(1, 0))
        v1.time = 1
        v2 = subj.Vehicle(2, subj.Point(1, 0))
        print(v1)
        self.assertEqual(subj.find_closest_vehicle(ride, time=0, vehicles=[v1, v2]), v2)
