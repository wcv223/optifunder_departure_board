from datetime import datetime
from typing import Dict, Tuple, List

import pytz
import requests
from requests.models import Response

from optifunder.settings import API_KEY


def fetch_predictions() -> Response:
    """
    Fetch prediction data from the MBTA API.

    :return: The HTTP response returned from the MBTA API.
    """
    base_url = 'https://api-v3.mbta.com/predictions'
    parameters = '?page%5Boffset%5D=0&page%5Blimit%5D=25&sort=departure_time&include=trip%2Cstop&filter%5Bdirection_id%5D=0&filter%5Broute_type%5D=2&filter%5Bstop%5D=place-sstat'
    headers = {'x-api-key': API_KEY}
    response = requests.get(base_url + parameters, headers=headers)
    return response


def process_included_data(included: List[Dict]) -> Tuple[Dict, Dict]:
    """
    Process the 'included' data from the MBTA API.

    :param included: A list of dictionaries containing 'trip' and 'stop' data.
    :return: A tuple containing two dictionaries, 'trips' and 'stops'.
    """
    trips = {}
    stops = {}
    for ele in included:
        if ele['type'] == 'trip':
            attributes = ele['attributes']
            trips[ele['id']] = {'headsign': attributes['headsign'], 'name': attributes['name']}
        elif ele['type'] == 'stop':
            platform_code = ele['attributes']['platform_code']
            stops[ele['id']] = {'platform_code': platform_code if platform_code else 'TBD'}
    return trips, stops


def process_predictions_data(data: List[Dict], trips: Dict, stops: Dict) -> List[Dict]:
    """
    Process the 'data' from the MBTA API into a list of predictions.

    :param data: A list of dictionaries containing 'prediction' data.
    :param trips: A dictionary of 'trip' data.
    :param stops: A dictionary of 'stop' data.
    :return: A list of dictionaries, each representing a prediction.
    """
    return [
        get_prediction_attributes(ele, trips, stops)
        for ele in data
    ]


def get_prediction_attributes(ele: Dict, trips: Dict, stops: Dict) -> Dict:
    """
    Create a dictionary of prediction attributes for a single prediction.

    :param ele: A dictionary representing a single prediction.
    :param trips: A dictionary of 'trip' data.
    :param stops: A dictionary of 'stop' data.
    :return: A dictionary of prediction attributes.
    """
    attributes = ele['attributes']
    status = attributes['status']
    departure_time = 'Departed' if status == 'Departed' else (
        'TBD' if not attributes['departure_time'] else convert_to_time_string(attributes['departure_time'])
    )
    trip_id = ele['relationships']['trip']['data']['id']
    stop_id = ele['relationships']['stop']['data']['id']
    return {
        'departure_time': departure_time,
        'headsign': trips[trip_id]['headsign'],
        'name': trips[trip_id]['name'],
        'platform_code': stops[stop_id]['platform_code'],
        'status': status,
    }


def convert_to_time_string(date_str: str) -> str:
    """
    Convert a date string to a time string.

    :param date_str: A string representing a date and time.
    :return: A string representing the time in '%I:%M %p' format.
    """
    date_obj = datetime.fromisoformat(date_str)
    return date_obj.strftime('%I:%M %p')
