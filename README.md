# finapi
A self-hosted REST API that scrapes data from Yahoo Finance.

### Dependencies
* BeautifulSoup
* Flask
* CORS
* Developed on Python 3.9.1

Use the following to check your current version of Python:
```
python --version
```

### Setting Targets
Head to Yahoo Finance and pick any symbol that you wish to scrape. From your browser's address bar, copy the part of the URL that appears after the forward slash that follows ``quote`` and before the question mark ``?``.
For example, if you want to scrape Bitcoin data from this page ```https://finance.yahoo.com/quote/BTC-USD?p=BTC-USD&.tsrc=fin-srch```, copy the ``BTC-USD`` portion and add it to your ``resources`` list in the server.py file.

Start the server from your command line using ``python server.py``


### Routes

#### Index (Default) route
When you run the command above you will see a message like this in your console:
```
Running on http://127.0.0.1:5001/
```
Navigate to that link, ``http://127.0.0.1:5001/`` to trigger the scraping process and you should get a JSON payload in return after a few seconds. While the server is running, you can make as many GET requests as you wish to this endpoint to keep getting fresh data. You can also use any other method, such as AJAX requests, to send GET requests to this endpoint to get a response.


#### Single route
```
http://127.0.0.1:5001/single/
```
You can use the single route to get information about only one symbol. It returns a JSON object similar to the other route. Also, like the default route, you can use any method you like to send GET requests to this route.

### Benefits
Since this is self hosted, you can make as many requests to the API as you wish without worrying about usage limits or service timeouts. You also do not need to pay for it, as is the case with almost all finance APIs available.

### Notes
The less items you have in your list (when using the default route), the more quickly you will get a response. You might be better off making multiple requests to /single.

### Sample JSON Response
Data is always returned in this format no matter what symbol you use (this is a response from the ``/single`` route. The default route will return more items):

```
{
    "status": "200",
    "response_datetime": "20-04-2021 20:32:22",
    "data": {
        "request_url": "https://finance.yahoo.com/quote/TSLA",
        "item_name": "Tesla, Inc. (TSLA)",
        "current_price": "718.99",
        "value_change": "4.36",
        "percent_change": "null",
        "volume": "35,609,035",
        "volume_24hr": "null",
        "volume_24hr_all_currencies": "null",
        "market_cap": "690.125B",
        "max_supply": "null",
        "circulating_supply": "null",
        "previous_close": "714.63",
        "open_price": "717.42",
        "bid": "712.15 x 1000",
        "ask": "715.00 x 2200",
        "day_range_lower": "710.68",
        "day_range_upper": "710.68",
        "f2_week_range": "134.76 - 900.40",
        "f2_week_range_lower": "134.76",
        "f2_week_range_upper": "134.76",
        "earnings_date": "Apr 26, 2021",
        "earnings_date_start": "Apr26,2021",
        "earnings_date_end": "Apr26,2021",
        "start_date": "null",
        "eps": "0.64",
        "forward_dividend_yeild": "N/A (N/A)"
    }
}
```
