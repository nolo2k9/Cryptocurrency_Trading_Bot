# Cryptocurrency_Trading_Bot

***About this application***
This application is a cryptocurrency trading bot that watches the Binance charts based on a coin pair you enter.
The application calcualates the Relative Strength Index (RSI) based on closing candles (default set to 14)
When the application is ran it constantly watches the price of your chosen coin pair.
It will then buy or sell currency on Binance depending on whether the coin is overbought or oversold.
If the coin is not overbought or oversold it will do nothing.
It Stores all of the saved closing prices and RSI values in lists.


# Pre-reqs:
Pip
# How to run project
Set up virtual environment:
https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/

Install requirements.txt:
pip3 install -r requirements.txt  

***References***

# Virtual environment
https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/

# TA_LIB
https://pypi.org/project/TA-Lib/

# Binance Api
https://github.com/sammchardy/python-binance

# RSI 
https://www.investopedia.com/terms/r/rsi.asp