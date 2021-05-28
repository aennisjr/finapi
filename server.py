from bs4 import BeautifulSoup
import requests
import time
import json
from datetime import datetime
from urllib.parse import urlparse

from flask import Flask, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

default_url = 'https://finance.yahoo.com/quote/'

# Set the time delay (in seconds) between requests for each resource - recommended: 2 seconds
resource_request_delay = 2

# Set the maximm number of seconds for the requests (by default, requests will wait indefinitely on the response)
timeout_secounds = 60

resources = [
	'V',
    'GME',
    '%5EGSPC',
    'AMC',
    'AAPL',			
    'BTC-USD',		# Crypto
    'TSLA',			# Stock
    'EURUSD%3DX' 	# Forex
]

def exception_check(value, index):
	try:
		value = value[index].get_text()
	except Exception as e:
		print(e)
		value = 'null'
	return value

def split_not_null(value, index):
	if(value != 'null' and value != ""):
		return value.split("-")[0].replace(" ", "")
	return 'null'

def if_not_null(value):
	if(value != 'null' and value != ""):
		return value
	return 'null'

def action(res):
	request = requests.get(default_url + res, timeout=timeout_secounds)
	soup = BeautifulSoup(request.content, 'html.parser')

	# Item Name
	item_name = exception_check(soup.find_all('h1', 'D(ib) Fz(18px)'), 0)

	# Item Start Date
	start_date = exception_check(soup.find_all('td', attrs={'data-test': lambda e: e.startswith('START_DATE-value') if e else False}), 0)

	# Item Volume
	volume = exception_check(soup.find_all('td', attrs={'data-test': lambda e: e.startswith('TD_VOLUME-value') if e else False}), 0)
	volume_24hr = exception_check(soup.find_all('td', attrs={'data-test': lambda e: e.startswith('TD_VOLUME_24HR-value') if e else False}), 0)
	volume_24hr_all_currencies = exception_check(soup.find_all('td', attrs={'data-test': lambda e: e.startswith('TD_VOLUME_24HR_ALLCURRENCY-value') if e else False}), 0)
	
	# Market Cap
	market_cap = exception_check(soup.find_all('td', attrs={'data-test': lambda e: e.startswith('MARKET_CAP-value') if e else False}), 0)

	# Circulating Supply
	circulating_supply = exception_check(soup.find_all('td', attrs={'data-test': lambda e: e.startswith('CIRCULATING_SUPPLY-value') if e else False}), 0)

	# Max Supply
	max_supply = exception_check(soup.find_all('td', attrs={'data-test': lambda e: e.startswith('MAX_SUPPLY-value') if e else False}), 0)

	# Current item price
	current_price = exception_check(soup.find_all('span', class_='Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'), 0)
	
	# Movement of price
	movement = exception_check(soup.find_all('span', attrs={'class': lambda e: e.startswith('Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) ') if e else False}), 0)
	
	# Capture change value & replace + sign (+ is not necessary)
	value_change = if_not_null(movement.split(" ")[0].replace("+", ""))

	# Replace (, ), and % to isolate numeric value
	percent_change = if_not_null(exception_check(movement.split(" "), 1).replace("%", "").replace("+", "").replace("(", "").replace(")", ""))

	# Previous close price
	previous_close = exception_check(soup.find_all('td', class_='Ta(end) Fw(600) Lh(14px)'), 0)

	# Open price
	open_price = exception_check(soup.find_all('td', attrs={'data-test': lambda e: e.startswith('OPEN-value') if e else False}), 0)

	# Bid price
	bid = exception_check(soup.find_all('td', attrs={'data-test': lambda e: e.startswith('BID-value') if e else False}), 0)

	# Ask price
	ask = exception_check(soup.find_all('td', attrs={'data-test': lambda e: e.startswith('ASK-value') if e else False}), 0)
	
	# Days Range - split into upper and lower
	days_range = exception_check(soup.find_all('td', attrs={'data-test': lambda e: e.startswith('DAYS_RANGE-value') if e else False}), 0)
	day_range_lower = split_not_null(days_range, 0)
	day_range_upper = split_not_null(days_range, 1)

	# 52 Week Range - split into upper and lower
	f2_week_range = exception_check(soup.find_all('td', attrs={'data-test': lambda e: e.startswith('FIFTY_TWO_WK_RANGE-value') if e else False}), 0)
	f2_week_range_lower = split_not_null(f2_week_range, 0)
	f2_week_range_upper = split_not_null(f2_week_range, 1)

	# Earnings Date Range - split into upper and lower
	earnings_date = exception_check(soup.find_all('td', attrs={'data-test': lambda e: e.startswith('EARNINGS_DATE-value') if e else False}), 0)
	earnings_date_start = split_not_null(earnings_date, 0)
	earnings_date_end = split_not_null(earnings_date, 1)

	# EPS (TTM)
	eps = exception_check(soup.find_all('td', attrs={'data-test': lambda e: e.startswith('EPS_RATIO-value') if e else False}), 0)

	# Forward Dividend Yeild
	forward_dividend_yeild = exception_check(soup.find_all('td', attrs={'data-test': lambda e: e.startswith('DIVIDEND_AND_YIELD-value') if e else False}), 0)

	''' Print statements for console if needed

	print("Item: " + item_name)
	print("Volume: " + volume)
	print("Volume (24hr): " + volume_24hr)
	print("Volume (24hr) All Currencies: " + volume_24hr_all_currencies)
	print("Market Cap: " + market_cap)
	print("Max Supply: " + max_supply)
	print("Circulating Supply: " + circulating_supply)
	print("Current Price: " + current_price)
	print("Percent Change: " + percent_change)
	print("Value Change: " + value_change)
	print("Previous Close: " + previous_close)
	print("Day Range Lower: " + day_range_lower)
	print("Day Range Upper: " + day_range_upper)
	print("52 Week Range Lower: " + f2_week_range_lower)
	print("52 Week Range Upper: " + f2_week_range_upper)
	print("Earnings Date Start: " + earnings_date_start)
	print("Earnings Date End: " + earnings_date_end)
	print("Start Date: " + start_date)
	print("EPS (TTM): " + eps)
	print("Forward Dividend Yeild: " + forward_dividend_yeild)
	print("")

	'''
	data = {
		'request_url': default_url + res,
		'item_name': item_name,
		'current_price': current_price,
		'value_change': value_change,
		'percent_change': percent_change,
		'volume': volume,
		'volume_24hr': volume_24hr,
		'volume_24hr_all_currencies': volume_24hr_all_currencies,
		'market_cap': market_cap,
		'max_supply': max_supply,
		'circulating_supply': circulating_supply,
		'previous_close': previous_close,
		'open_price': open_price,
		'bid': bid,
		'ask': ask,
		'day_range_lower': day_range_lower,
		'day_range_upper': day_range_upper,
		'f2_week_range': f2_week_range,
		'f2_week_range_lower': f2_week_range_lower,
		'f2_week_range_upper': f2_week_range_upper,
		'earnings_date': earnings_date,
		'earnings_date_start': earnings_date_start,
		'earnings_date_end': earnings_date_end,
		'start_date': start_date,
		'eps': eps,
		'forward_dividend_yeild': forward_dividend_yeild
	}

	return data

	# Delay the repetition of the requests by n (resource_request_delay) seconds
	time.sleep(-time.time() % resource_request_delay)


@app.route('/', methods=['GET'])
def index():
	
	all_data = list()
	json_data = list()

	for res in resources:
	    all_data.append(action(res))

	# Encode data in JSON format
	now = datetime.now()
	
	pre = {'status': '200', 'response_datetime': now.strftime("%d-%m-%Y %H:%M:%S"), 'data': all_data}
	json_data = json.dumps(pre)

	# Decode and Print
	response = Response(json_data, content_type="application/json; charset=utf-8" )
	return response

@app.route('/single/')
@app.route('/single/<res>', methods=['GET'])
def single(res):
	
	single_data = list()
	json_data = list()

	single_data = action(res)
	# Encode data in JSON format
	now = datetime.now()
	
	pre = {'status': '200', 'response_datetime': now.strftime("%d-%m-%Y %H:%M:%S"), 'data': single_data}
	json_data = json.dumps(pre)

	# Decode and Print
	response = Response(json_data, content_type="application/json; charset=utf-8" )
	return response

if __name__ == '__main__':
    app.run(debug=True, port=5001)