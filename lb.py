from lbcapi import api
import requests
import json
import pandas as pd
import datetime

#hmac_key = Your HMAC key here
#hmac_secret = Your HMAC secret here

conn = api.hmac("a","b")
list_coins = ["VED","COP","USD"]
for coin in list_coins:
    CURRENCY = coin
    df = pd.DataFrame(columns=['date', 'tid','price','amount'])

    for i in range(1, 20000):
        try:
            if i == 1:
                params = {'max_tid': '10053923389'}
                print(i)
            else:
                params = {'max_tid': new_tid}
                print(i)
                print(new_tid)
                print(f"working on {coin}")

            response = conn.call('GET', f'/bitcoincharts/{coin}/trades.json', params=params).json()
            df = df.append(response)
            new_tid = df[-1:]['tid'] - 1

        except Exception:
         pass
    df['date_formatted'] = df['date'].apply(lambda d: datetime.datetime.fromtimestamp(d))
    df['StableCoin'] = CURRENCY
    df['date_yyyy_mm_dd'] = df.date_formatted.apply(lambda x: x.strftime('%Y%m%d')).astype(int)
    df.columns = ['date', 'tid', 'price', 'amount', 'date_formatted','sc_fiat', 'date_yyyy_mm_dd']
    df.to_csv(f"{coin}.csv", mode='a', index=False, header=False)
