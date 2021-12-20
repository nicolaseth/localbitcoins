import yfinance as yf
import pandas as pd
from datetime import datetime

#set variables
start = datetime(2017, 5, 1)
end = datetime(2021, 12, 13)
symbol = "BTC-USD"

df_y = yf.download(symbol,start=start, end=end)


