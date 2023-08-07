from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import render
from requests.exceptions import RequestException

from departure_board.helpers import fetch_predictions, process_included_data, process_predictions_data


def board(request: HttpRequest) -> HttpResponse:
    """
    Handles requests to display the departure board.

    This function fetches prediction data, processes it, and passes it to the
    'board.html' template for rendering.

    :param request: An HttpRequest object.
    :return: An HttpResponse object for the 'board.html' template.
    :raises: JsonResponse with status 500 if unable to reach the API.
    """
    try:
        response = fetch_predictions()
        response.raise_for_status()
    except RequestException as e:
        return JsonResponse({"error": "Unable to reach the API"}, status=500)

    response_data = response.json()
    data = response_data['data']
    included = response_data['included']

    trips, stops = process_included_data(included)
    predictions = process_predictions_data(data, trips, stops)

    return render(request, 'board.html', {'predictions': predictions})
