"""
Tests RaceData.py.
"""
import unittest
from unittest.mock import patch, sentinel

from replayenhancer.RaceData import RaceData, Driver


class TestRaceData(unittest.TestCase):
    """
    Tests against the RaceData object.
    """
    @patch('replayenhancer.RaceData.TelemetryData', autospec=True)
    def test_init(self, mock_telemetry):
        mock_telemetry.return_value = sentinel.telemetry_data

        instance = RaceData(sentinel.directory)
        expected_result = RaceData
        self.assertIsInstance(instance, expected_result)

    @patch('replayenhancer.RaceData.TelemetryData', autospec=True)
    def test_property_classification(self, mock_telemetry):
        mock_telemetry.return_value = sentinel.telemetry_data

        instance = RaceData(sentinel.directory)
        expected_result = list
        self.assertIsInstance(instance.classification, expected_result)

    @patch('replayenhancer.RaceData.TelemetryData', autospec=True)
    def test_property_current_drivers(self, mock_telemetry):
        mock_telemetry.return_value = sentinel.telemetry_data

        instance = RaceData(sentinel.directory)
        expected_result = list
        self.assertIsInstance(instance.current_drivers, expected_result)

    @unittest.skip("Further implementation needed.")
    def test_property_driver_name_lookup_new(self):
        pass

    @unittest.skip("Further implementation needed.")
    def test_property_driver_name_lookup_existing(self):
        pass

    @unittest.skip("Depends on driver_name lookup."
                   "Further implementation needed.")
    def test_property_drivers(self):
        pass

    @patch('replayenhancer.RaceData.TelemetryData', autospec=True)
    def test_property_elapsed_time(self, mock_telemetry):
        mock_telemetry.return_value = sentinel.telemetry_data

        instance = RaceData(sentinel.directory)
        expected_result = float
        self.assertIsInstance(instance.elapsed_time, expected_result)

    @unittest.skip("Further implementation needed.")
    def test_property_starting_grid(self):
        pass

    @patch('replayenhancer.RaceData.TelemetryData', autospec=True)
    def test_property_telemetry_data(self, mock_telemetry):
        mock_telemetry.return_value = sentinel.telemetry_data

        instance = RaceData(sentinel.directory)
        expected_result = sentinel.telemetry_data
        self.assertEqual(instance.telemetry_data, expected_result)

    @unittest.skip("Further implementation needed.")
    def test_method_get_data(self):
        pass


class TestDriver(unittest.TestCase):
    """
    Unit tests for Driver object.
    """
    def test_init(self):
        instance = Driver(sentinel.index, sentinel.name)
        expected_result = Driver
        self.assertIsInstance(instance, expected_result)

    def test_property_index(self):
        instance = Driver(sentinel.index, sentinel.name)
        expected_result = sentinel.index
        self.assertEqual(instance.index, expected_result)

    def test_property_name(self):
        instance = Driver(sentinel.index, sentinel.name)
        expected_result = sentinel.name
        self.assertEqual(instance.name, expected_result)

    def test_property_real_name_default(self):
        instance = Driver(sentinel.index, sentinel.name)
        expected_result = sentinel.name
        self.assertEqual(instance.real_name, expected_result)

    def test_property_real_name_setter(self):
        instance = Driver(sentinel.index, sentinel.name)
        instance.real_name = sentinel.real_name
        expected_result = sentinel.real_name
        self.assertEqual(instance.real_name, expected_result)

    @patch('replayenhancer.RaceData.SectorTime', autospec=True)
    def test_method_add_sector_time_no_previous(self, sector_time):
        instance = Driver(sentinel.index, sentinel.name)
        sector_time.time = -123.0
        sector_time.sector = 1
        sector_time.invalid = False

        instance.add_sector_time(sector_time)

        self.assertEqual(len(instance._sector_times), 0)

    @patch('replayenhancer.RaceData.SectorTime', autospec=True)
    def test_method_add_sector_time_first(self, sector_time):
        instance = Driver(sentinel.index, sentinel.name)
        sector_time.time = sentinel.time
        sector_time.sector = 1
        sector_time.invalid = False

        instance.add_sector_time(sector_time)

        self.assertEqual(len(instance._sector_times), 1)

    @patch('replayenhancer.RaceData.SectorTime', autospec=True)
    def test_method_add_sector_time_duplicate(self, sector_time):
        instance = Driver(sentinel.index, sentinel.name)
        sector_time.time = sentinel.time
        sector_time.sector = 1
        sector_time.invalid = False

        instance.add_sector_time(sector_time)
        instance.add_sector_time(sector_time)

        self.assertEqual(len(instance._sector_times), 1)

    def test_method_add_sector_time_invalidate_first_lap(self):
        instance = Driver(sentinel.index, sentinel.name)
        sectors = [
            (sentinel.time_1, 1, False),
            (sentinel.time_2, 2, False),
            (sentinel.time_3, 3, True)]
        for time, sector, invalid in sectors:
            with patch(
                    'replayenhancer.RaceData.SectorTime',
                    autospec=True) as SectorTime:
                sector_time = SectorTime(time, sector, invalid)
                sector_time.sector = sector
                sector_time.time = time
                sector_time.invalid = invalid

                instance.add_sector_time(sector_time)

        self.assertEqual(len(instance._sector_times), len(sectors))
        self.assertTrue(all([sector_time.invalid for sector_time in instance._sector_times]))

    def test_method_add_sector_time_invalidate_later_lap(self):
        instance = Driver(sentinel.index, sentinel.name)
        sectors = [
            (sentinel.time_1, 1, False),
            (sentinel.time_2, 2, False),
            (sentinel.time_3, 3, False),
            (sentinel.time_4, 1, False),
            (sentinel.time_5, 2, True),
            (sentinel.time_6, 3, True)]
        for time, sector, invalid in sectors:
            with patch(
                    'replayenhancer.RaceData.SectorTime',
                    autospec=True) as SectorTime:
                sector_time = SectorTime(time, sector, invalid)
                sector_time.sector = sector
                sector_time.time = time
                sector_time.invalid = invalid

                instance.add_sector_time(sector_time)

        # First lap should still be valid.
        result = [
            sector_time.invalid
            for sector_time in instance._sector_times[:3]]
        self.assertTrue(not any(result))

        # Second lap should be invalid.
        result = [
            sector_time.invalid
            for sector_time in instance._sector_times[3:]]
        self.assertTrue(all(result))


if __name__ == "__main__":
    unittest.main()
