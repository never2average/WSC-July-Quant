# Wall Street Quant Challenge


##### This is a very introductory level repository for coders trying to move into the field of finance.


What is an alpha?

An alpha is basically a mathematical formula that assigns your investment money into various stocks.


So, in this repository we will be assigning money to our stocks in proportion to our bucket of stocks in proportion to the lot size of one option of that stock.

Example:
Ticker | Lot Size | Weight in portfolio 
HINDALCO| 2000 | 0.2
BAJAJFINSV | 3000|
ITC | 1000 | 0.1
TITAN | 2000 | 0.2
TECHM | 2000 | 0.2




### Setup:

1. Firstly go to quandl.com and make an account there. This will allow you to use their API key for automatic data retrieval from python.

2. Open your terminal and type in the following commands
```bash
	git clone https://github.com/never2average/WSCQuant.git
	cd WSCQuant
	python3 -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt
```
3. Open config.py and paste in the API key that you recieved from quandl in the field key, otherwise there will be an error

4. Run portfolio.py and drawdown.py
```bash
python3 portfolio.py
python3 drawdown.py
```

PS: It is recommended that you use jupyter notebook or spyder
