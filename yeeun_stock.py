# %matplotlib inline
import FinanceDataReader as fdr
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker
from mplfinance.original_flavor import candlestick2_ochl

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


# df_kospi = df_simple[df_simple['Market'].isin(['KOSPI'])]
# df_kosdaq = df_simple[df_simple['Market'].isin(['KOSDAQ'])]
# df_specific = fdr.DataReader('068270', '2021-01-22')
# print(int(df_specific['Close'][0]))
# 어제 종가  추출하기
# df_specific 에 종목번호, 어제  날짜 넣음
# df_specific['Close'][0] 으로 어제 종가만 추출가능 -> int로 캐스팅하기

# 가격 그래프 그리기
# df = fdr.DataReader('KS11', '2021-01-15')
# df['Close'].plot()
# plt.show()

# df = fdr.DataReader('215600', '2018')
# print(df.head(10))




# 봉차트 그리기
df_specific = fdr.DataReader('005930', '2020-08-20')
print(df_specific)

df_specific['MA3'] = df_specific['Close'].rolling(3).mean()
df_specific['MA5'] = df_specific['Close'].rolling(5).mean()
df_specific['MA10'] = df_specific['Close'].rolling(10).mean()
df_specific['MA60'] = df_specific['Close'].rolling(60).mean()
df_specific[['Close','MA3','MA5','MA10']].plot()


fig = plt.figure(figsize=(20,10))
ax = fig.add_subplot(111)
index = df_specific.index.astype('str') # 캔들스틱 x축이 str로 들어감

# 이동평균선 그리기
ax.plot(index, df_specific['MA3'], label='MA3', linewidth=0.7)
ax.plot(index, df_specific['MA5'], label='MA5', linewidth=0.7)
ax.plot(index, df_specific['MA10'], label='MA10', linewidth=0.7)

# X축 티커 숫자 20개로 제한
ax.xaxis.set_major_locator(ticker.MaxNLocator(20))

# 그래프 title과 축 이름 지정
# ax.set_title(stock_name, fontsize=22)
ax.set_xlabel('Date')

# 캔들차트 그리기
candlestick2_ochl(ax, df_specific['Open'], df_specific['High'],
                  df_specific['Low'], df_specific['Close'],
                  width=0.5, colorup='r', colordown='b')
ax.legend()
plt.grid()
plt.show()