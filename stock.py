# %matplotlib inline

import matplotlib.pyplot as plt
import FinanceDataReader as fdr
fdr.__version__


plt.rcParams["figure.figsize"] = (14,4)
plt.rcParams['lines.linewidth'] = 2
plt.rcParams["axes.grid"] = True

df_krx = fdr.StockListing('KRX')
print(df_krx.iloc[:, [0,1,2]])
# df = fdr.DataReader('KS11', '1984')
# df['Close'].plot()
# plt.show()
#
# df = fdr.DataReader('215600', '2018')
# print(df.head(10))