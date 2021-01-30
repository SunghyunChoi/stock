# %matplotlib inline
import FinanceDataReader as fdr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker
from mplfinance.original_flavor import candlestick2_ochl
import os
import sys
#sys.path.append(os.path.dirname())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stock.settings")
import django
django.setup()
from exchange.models import Stock_list
from datetime import datetime

df_kospi = fdr.StockListing('KOSPI')
df_simple = df_kospi.iloc[:, [0, 1, 2]]  # 종목번호, 마켓, 종목이름
today = datetime.today().strftime('%Y-%m-%d')
stock_list = Stock_list.objects.all()
for one in stock_list:
    stock_id = str(one.symbol)
    df_specific = fdr.DataReader(stock_id, today)
    try:
        print(df_specific)
        one.cur_price = int(df_specific['Close'][0])
        one.save()
    except:
        print("ERROR")
        print(df_specific)
    