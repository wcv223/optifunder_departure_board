from unittest.mock import patch, Mock
from django.test import TestCase
from departure_board.helpers import fetch_predictions, process_included_data, get_prediction_attributes, convert_to_time_string, \
    get_current_boston_time


class DepartureBoardTests(TestCase):

    @patch('departure_board.helpers.requests.get')
    def test_fetch_predictions(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        response = fetch_predictions()
        self.assertEqual(response.status_code, 200)
        mock_get.assert_called_once()

    def test_process_included_data(self):
        included_data = [
            {
                'type': 'trip',
                'id': '1',
                'attributes': {'headsign': 'Test1', 'name': 'Test1'},
            },
            {
                'type': 'stop',
                'id': '2',
                'attributes': {'platform_code': 'Test2'},
            },
        ]

        expected_trips = {'1': {'headsign': 'Test1', 'name': 'Test1'}}
        expected_stops = {'2': {'platform_code': 'Test2'}}

        trips, stops = process_included_data(included_data)
        self.assertEqual(trips, expected_trips)
        self.assertEqual(stops, expected_stops)

    def test_get_prediction_attributes(self):
        ele = {
            'attributes': {'status': 'Departed'},
            'relationships': {'trip': {'data': {'id': '1'}}, 'stop': {'data': {'id': '2'}}}
        }
        trips = {'1': {'headsign': 'Test1', 'name': 'Test1'}}
        stops = {'2': {'platform_code': 'Test2'}}
        expected_result = {
            'departure_time': 'Departed',
            'headsign': 'Test1',
            'name': 'Test1',
            'platform_code': 'Test2',
            'status': 'Departed',
        }

        result = get_prediction_attributes(ele, trips, stops)
        self.assertEqual(result, expected_result)

    def test_convert_to_time_string(self):
        date_str = "2023-07-27T13:45:00"
        expected_result = "01:45 PM"
        result = convert_to_time_string(date_str)
        self.assertEqual(result, expected_result)

    def test_get_current_boston_time(self):
        time_now, date_now = get_current_boston_time()
        self.assertIsNotNone(time_now)
        self.assertIsNotNone(date_now)
