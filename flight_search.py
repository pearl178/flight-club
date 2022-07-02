import datetime as dt
import requests
from flight_data import FlightData


class FlightSearch:
    def __init__(self):
        self.END_POINT = 'https://tequila-api.kiwi.com/'
        self.header = {
            'apikey': 'gu3ZrG3H8OXk1DfvSb_22Rra1pJw-Wkf'
        }
        self.city_codes = []

    def get_city_codes(self, city_names):
        for n in range(len(city_names)):
            tequila_parameters = {
                'term': city_names[n],
                'location_types': 'city',
                'limit': 1
            }
            tequila_response = requests.get(url=f"{self.END_POINT}locations/query", headers=self.header,
                                            params=tequila_parameters)
            city_code = tequila_response.json()['locations'][0]['code']
            self.city_codes.append(city_code)
        return self.city_codes

    def get_lowest_price(self, origin_city_code, destination_city_code, date_from, date_to):
        flight_data = None
        try:
            search_parameters = {
                'fly_from': origin_city_code,
                'fly_to': destination_city_code,
                'date_from': date_from,
                'date_to': date_to,
                "nights_in_dst_from": 7,
                "nights_in_dst_to": 28,
                'flight_type': 'round',
                'curr': 'USD',
                'max_stopovers': 0,
                'limit': 1
            }
            response = requests.get(url=f"{self.END_POINT}search", headers=self.header, params=search_parameters)
            flight_info = response.json()['data'][0]
            flight_data = FlightData(
                price=flight_info['price'],
                origin_city=flight_info['route'][0]['cityFrom'],
                origin_airport=flight_info['route'][0]['flyFrom'],
                destination_city=flight_info['route'][0]['cityTo'],
                destination_airport=flight_info['route'][0]['flyTo'],
                out_date=dt.datetime.fromtimestamp(flight_info['route'][0]['dTime']),
                return_date=dt.datetime.fromtimestamp(flight_info['route'][1]['dTime']),
            )
        except:
            search_parameters = {
                'fly_from': origin_city_code,
                'fly_to': destination_city_code,
                'date_from': date_from,
                'date_to': date_to,
                "nights_in_dst_from": 7,
                "nights_in_dst_to": 28,
                'flight_type': 'round',
                'curr': 'USD',
                'max_stopovers': 1,
                'limit': 1
            }
            response = requests.get(url=f"{self.END_POINT}search", headers=self.header, params=search_parameters)
            flight_info = response.json()['data'][0]
            flight_data = FlightData(
                price=flight_info['price'],
                origin_city=flight_info['route'][0]['cityFrom'],
                origin_airport=flight_info['route'][0]['flyFrom'],
                destination_city=flight_info['route'][1]['cityTo'],
                destination_airport=flight_info['route'][1]['flyTo'],
                out_date=dt.datetime.fromtimestamp(flight_info['route'][0]['dTime']),
                return_date=dt.datetime.fromtimestamp(flight_info['route'][3]['dTime']),
                stop_overs=1,
                via_city=flight_info['route'][0]['cityTo']
            )
        finally:
            return flight_data
