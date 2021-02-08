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
from datetime import datetime, timedelta

df_kospi = fdr.StockListing('KOSPI')
df_simple = df_kospi.iloc[:, [0, 1, 2]]  # 종목번호, 마켓, 종목이름

# 실행시킬때마다 오늘 종가기준 가격 업데이트
# 토,일에 실행할 경우, empty dataframe 때문에 오류 발생하므로 cron 설정 시 월~금만 실행하도록 설정할 것
# cron 설정은 서버에서 해야하므로 통키와 상의해볼 것
today = datetime.today().strftime('%Y-%m-%d')
past = (datetime.today() - timedelta(days=10)).strftime('%Y-%m-%d')
stock_list = Stock_list.objects.all()
for i in range(len(stock_list)):
    stock_id = str(stock_list[i].symbol)
    try:
        df_specific = fdr.DataReader(stock_id, past, today) # 속도 향상을 위해 10일치만 추출
        stock_list[i].cur_price = int(df_specific['Close'][0])
        stock_list[i].save()
        print(stock_list[i].stock_name, stock_list[i].cur_price, "good\n")
    except ValueError:
        print("ValueError", stock_list[i].stock_name)
        # print(df_specific)
        pass
    except KeyError:
        print("KeyError", stock_list[i].stock_name)
        # print(df_specific)
        pass

