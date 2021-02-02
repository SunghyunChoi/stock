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
from mplfinance.original_flavor import candlestick2_ohlc
df_kospi = fdr.StockListing('KOSPI')
df_simple = df_kospi.iloc[:, [0,1,2]] # 종목번호, 마켓, 종목이름
#print(df_simple)
# for i in range(len(df_simple)):
#     stocks_data = df_simple.iloc[i]
#     name = str(stock_data['Name'])
#     symbol = str(stock_data['Symbol'])
#     try:
#        a = Stock_list(stock_name = name, symbol = symbol, market_name = "KOSPI", cur_price = '0')
#        a.save()
#     except:
#        continue

# if __name__ == '__main__':
#     print("hi")
#
#
# for one in Stock_list:
#     print(Stock_list.symbol)



fdr.__version__


plt.rcParams["figure.figsize"] = (14,4)
plt.rcParams['lines.linewidth'] = 2
plt.rcParams["axes.grid"] = True

df_krx = fdr.StockListing('KRX')
df_simple = df_krx.iloc[:, [0,1,2]] # 종목번호, 마켓, 종목이름

# 이름으로 종목 번호 검색해서 가격 데이터 추출하기
# stock_name으로 종목명 받으면 stock_id로 종목번호 구하기
stock_name = '삼성전자'
stock_name_table = df_simple[df_simple['Name'] == stock_name]
stock_id = stock_name_table.iloc[0, 0]



kospi_df = fdr.DataReader('000020', '2020-08-01')
fig = plt.figure(figsize=(20,10))
ax = fig.add_subplot(111)
index = kospi_df.index.astype('str') # 캔들스틱 x축이 str로 들어감

# X축 티커 숫자 20개로 제한
ax.xaxis.set_major_locator(ticker.MaxNLocator(20))

# 그래프 title과 축 이름 지정
ax.set_title('KOSPI INDEX', fontsize=22)
ax.set_xlabel('Date')


# 캔들차트 그리기
candlestick2_ohlc(ax, kospi_df['Open'], kospi_df['High'],
                  kospi_df['Low'], kospi_df['Close'],
                  width=0.5, colorup='k', colordown='r')
ax.legend()
plt.grid()
plt.show()

