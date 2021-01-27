import os
## Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로를 등록합니다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stock.settings")
## 이제 장고를 가져와 장고 프로젝트를 사용할 수 있도록 환경을 만듭니다.
import django
django.setup()

from exchange.models import Stock_list
# %matplotlib inline
import FinanceDataReader as fdr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker
from mplfinance.original_flavor import candlestick2_ochl
df_kospi = fdr.StockListing('KOSPI')
df_simple = df_kospi.iloc[:, [0,1,2]] # 종목번호, 마켓, 종목이름

#print(df_simple)

for i in range(len(df_simple)):
    stock_data = df_simple.iloc[i]
    name = str(stock_data['Name'])
    symbol = str(stock_data['Symbol'])
    try:
       a = Stock_list(stock_name = name, symbol = symbol, market_name = "KOSPI", cur_price = '0')
       a.save()
    except:
       continue
    