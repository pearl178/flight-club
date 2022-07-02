import datetime as dt
from notifier import Notifier
from data_manager import DataManager
from flight_search import FlightSearch


data_manager = DataManager()
flight_search = FlightSearch()
notifier = Notifier(data_manager.get_user_emails())

ORIGIN_CITY_CODE = 'SLC'
tomorrow = dt.date.today() + dt.timedelta(days=1)
six_month_from_now = dt.date.today() + dt.timedelta(days=60)


city_names = data_manager.get_city_names()

# Use this line to populate IATA Code for the first run
# city_codes = flight_search.get_city_codes(city_names)
# data_manager.fill_sheet_codes(city_codes)

# Use this line when IATA Code column is already populated
city_codes = data_manager.get_city_codes()

city_code_current_price = data_manager.get_current_prices()

i = 1
for city_code in city_codes:
    i += 1
    flight_data = flight_search.get_lowest_price(ORIGIN_CITY_CODE, city_code, tomorrow, six_month_from_now)
    if flight_data is None:
        continue
    else:
        price = flight_data.price
        if price < city_code_current_price[city_code]:
            data_manager.post_new_price(i, price)
            if flight_data.stop_overs == 0:
                message = f'Low price alert! Only ${flight_data.price} from {flight_data.origin_city}' \
                          f'-{flight_data.origin_airport} to {flight_data.destination_city}-{flight_data.destination_airport},' \
                          f'from {flight_data.out_date} to {flight_data.return_date}'
            else:
                message = f'Low price alert! Only ${flight_data.price} from {flight_data.origin_city}' \
                          f'-{flight_data.origin_airport} to {flight_data.destination_city}-{flight_data.destination_airport},' \
                          f'from {flight_data.out_date} to {flight_data.return_date}\nFlight has 1 stop over, via {flight_data.via_city}'
            notifier.send_emails(message)
            print(message)



