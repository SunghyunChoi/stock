import FinanceDataReader as fdr
import pandas as pd
import ssl,certifi
import matplotlib.pyplot as plt
# plt.rcParams["font.family"] = 'nanummyeongjo'
# plt.rcParams["figure.figsize"] = (14,4)
# plt.rcParams['lines.linewidth'] = 2
# plt.rcParams["axes.grid"] = True

# df = fdr.DataReader('005930','2020-06-01','2020-06-30')
# # print(df)
# df.plot()

# sp500 = fdr.StockListing('S&P500')
# sp500.tail()
df = fdr.DataReader('AAPL', '2020')
df['Close'].plot()
plt.show()
