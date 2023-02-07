import yfinance as yf
import matplotlib.pyplot as plt
from scipy.stats import norm
import matplotlib.mlab as mlab
import numpy as np
from numpy import trapz
import seaborn as sns
import time
from random import choices

ticker = 'AAPL'

# Get the data for the stock AAPL
spy_data = yf.download(ticker, '1960-01-01', '2019-08-01')

daily_change = spy_data['Adj Close'].pct_change()

# filter out non-finite values
daily_change = np.array(daily_change)
daily_change = daily_change[np.isfinite(daily_change)]

hist = sns.histplot(data=daily_change, bins=201, kde=True, stat='density')

plt.show()

line = hist.lines[0]
x, y = line.get_data()

# save data to csv file
np.savetxt(f'{ticker}_price_distribution_data.csv', np.column_stack((x, y)), delimiter=',', header='x,y')
