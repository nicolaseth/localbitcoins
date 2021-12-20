#!/usr/bin/env python
# coding: utf-8

# In[477]:


import pandas as pd
import numpy as np
from datetime import datetime
import datetime
#df_BTC = pd.read_csv("BTC.csv")
df_COP = pd.read_csv("/Users/nicolasmartinez/PycharmProjects/localbitcoins/COP.csv", index_col=False)
df_USD = pd.read_csv("/Users/nicolasmartinez/PycharmProjects/localbitcoins/USD.csv", index_col=False)
df_COP.columns = ['date', 'tid', 'price', 'amount', 'date_formatted','sc_fiat', 'date_yyyy_mm_dd']
df_USD.columns = ['date', 'tid', 'price', 'amount', 'date_formatted','sc_fiat', 'date_yyyy_mm_dd']


result = df_USD.append(df_COP, sort=False)


df_duplicates = result[result["date_yyyy_mm_dd"]>=20141125]# got the df with the same dates
#df_duplicates = df_duplicates[df_duplicates["amount"].duplicated(keep=False)]#getting only the duplicates
df_duplicates = df_duplicates[df_duplicates.duplicated('amount')]
df_duplicates['lenAm'] = df_duplicates['amount'].astype(str).map(len)# getting the length of the amount.  We'll work matching transaction up to the 8 decimal.
df_duplicates['date_formatted'] = pd.to_datetime(df_duplicates['date_formatted'], format = '%Y-%m-%d')


df_duplicates = df_duplicates[df_duplicates["lenAm"]>=10]# working only amounts with 8 decimals - A Satoshi
df_duplicates =df_duplicates.sort_values(["date_yyyy_mm_dd", "amount"], ascending=[True, True])# organizing the amounts to compare times
df_duplicates["shift_date"] = df_duplicates["date_formatted"].shift(1)
df_duplicates["shift_amount"] = df_duplicates["amount"].shift(1)

df_duplicates["zero_amt"] = df_duplicates["amount"] - df_duplicates["shift_amount"]
df_duplicates["shift_amount_up"] = df_duplicates["zero_amt"].shift(-1)
df_duplicates["less5"] = df_duplicates["date_formatted"] - df_duplicates["shift_date"]
df_duplicates["less5"] = df_duplicates['less5'] / np.timedelta64(1, 'h')
df_duplicates["less5"] = df_duplicates['less5'].abs()
df_duplicates["Curr_Dest"] = df_duplicates["sc_fiat"].shift(-1)

df_duplicates




# In[557]:





# temp_df

# In[556]:


temp_df.size


# In[558]:


temp_df = df_duplicates.loc[((df_duplicates['less5'] <=5) &
                         (df_duplicates['zero_amt'] == 0))] 


temp_df =temp_df.sort_values(["date_yyyy_mm_dd", "amount"], ascending=[True, True])
temp_df


# In[559]:


temp_df.size/result.size #percentage of transactions of the total that are transfer vehicles


# In[481]:





# In[482]:


temp_df['Date'] = temp_df['date'].apply(lambda d: datetime.datetime.fromtimestamp(int(d)).strftime('%Y-%m-%d'))


# In[ ]:





# In[404]:





# In[484]:


column = temp_df["date_yyyy_mm_dd"]
max_value = column.min()
print(max_value)


# In[ ]:





# In[485]:


transfer_df = temp_df[temp_df['sc_fiat']!=temp_df['Curr_Dest']] 


# In[457]:





# In[ ]:





# In[543]:


import yfinance as yf
import pandas as pd
from datetime import datetime

#set variables
start = datetime(2017, 5, 1)
end = datetime(2021, 12, 13)
symbol = "BTC-USD"

df_y= yf.download(symbol,start=start, end=end,)

#print(df_y.info())

dfy_close = df_y.drop(columns=['Open', 'High','Low','Close','Volume'])


# In[505]:


df_c = dfy_close.reset_index(drop=False)


# In[506]:


transfer_df_copy = transfer_df.copy()


# In[507]:





# In[508]:


transfer_df_copy['Date'] = pd.to_datetime(transfer_df_copy['Date'])
df_c['Date'] = pd.to_datetime(df_c['Date'])
df_c = df_c.sort_values('Date')
transfer_df_copy = transfer_df_copy.sort_values('Date')

df_usa_col = pd.merge_asof(transfer_df_copy, df_c, on='Date')


# In[509]:


df_usa_col['transfer_USD'] = df_usa_col['amount']*df_usa_col['Adj Close']


# In[ ]:





# In[513]:


df_usa_col.groupby('Date').agg({'transfer_USD' : 'sum'})# grouping total transfers from Both Countries by Date (daily)


# In[547]:


df_usa_col_summary = df_usa_col.describe()


# In[553]:





# In[549]:


df_usa_col_summary.to_csv("summaryTotalTransfersCOPUSD.csv")#exporting the describe DF


# In[ ]:





# In[530]:


df_COP_to_USD = df_usa_col.query('sc_fiat == "COP"')
df_COP_to_USD


# In[554]:


df_COP_to_USD_sum = df_usa_col.describe()


# In[555]:


df_COP_to_USD_sum


# In[532]:


df_COP_to_USD = df_COP_to_USD.groupby('Date').agg({'transfer_USD' : 'sum'})# grouping total transfers by Date (dailyy)
df_COP_to_USD


# In[524]:


df_COP_to_USD.to_csv("transfersfromCOPtoUSD.csv")


# In[538]:


df_USD_to_COP = df_usa_col.query('sc_fiat == "USD"')
df_USD_to_COP


# In[539]:


df_COP_to_USD = df_USD_to_COP.groupby('Date').agg({'transfer_USD' : 'sum'})


# In[540]:


df_COP_to_USD


# In[542]:



df_COP_to_USD.to_csv("transfersfromUSDtoCOP.csv")


# In[ ]:




