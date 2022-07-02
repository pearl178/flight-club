import requests

class DataManager:
    def __init__(self):
        self.END_POINT = 'https://api.sheety.co/f266fc6da30b4c5d27abf38dbec08fea/flightDeals/prices'
        self.END_POINT_USER = 'https://api.sheety.co/f266fc6da30b4c5d27abf38dbec08fea/flightDeals/users'
        self.response = requests.get(url=f"{self.END_POINT}")
        self.response_users = requests.get(url=f"{self.END_POINT_USER}")
        self.rows = self.response.json()['prices']
        self.user_rows = self.response_users.json()['users']

    def get_city_names(self):
        city_names = [row['city'] for row in self.rows]
        return city_names

    def get_city_codes(self):
        city_codes = [row['iataCode'] for row in self.rows]
        return city_codes

    def get_current_prices(self):
        city_code_current_price = {row['iataCode']: row['lowestPrice'] for row in self.rows}
        return city_code_current_price

    def get_user_emails(self):
        emails = [user_row['email'] for user_row in self.user_rows]
        return emails

    def fill_sheet_codes(self, city_codes):
        for n in range(len(city_codes)):
            sheety_parameters = {
                'price':
                    {
                        'iataCode': city_codes[n]
                    }
            }
            id_num = n + 2
            requests.put(url=f"{self.END_POINT}/{id_num}", json=sheety_parameters)

    def post_new_price(self, id, new_price):
        sheety_parameters = {
            'price':
                {
                    'lowestPrice': new_price
                }
        }
        requests.put(url=f"{self.END_POINT}/{id}", json=sheety_parameters)