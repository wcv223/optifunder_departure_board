# Departure Board project for OptiFunder

The goal of this Django project is to creat a departure board using the Massachusetts Bay Transportation Authority 
(MBTA) V3 API. This project uses real-time information by making a GET request using the Predictions call. More 
information on the MBTA V3 API can be found at https://api-v3.mbta.com/docs/swagger/index.html. 

## Setup

1. Clone this repository
2. Create a new virtual environment 
3. Install requirements 
4. Request your own MBTA API key from https://api-v3.mbta.com
5. Create a .env file at the root level of the project
6. Add your API key to the .env file EX.`API_KEY=Your Key`
7. Start the server: `python manage.py runserver`
8. Access site at http://127.0.0.1:8000/departure_board/