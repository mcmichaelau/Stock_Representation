import yfinance as yf
import matplotlib.pyplot as plt
from scipy.stats import norm
import matplotlib.mlab as mlab
import numpy as np
from numpy import trapz
import seaborn as sns
import time
from random import choices
import math


def get_prices(ticker, length):
    # ticker (all caps)
    ticker = ticker

    # read distribution values from csv file
    x, y = np.loadtxt(f'{ticker}_price_distribution_data.csv', delimiter=',', skiprows=1, unpack=True)

    # generate new data
    new_price_change_data = (choices(x, y, k=1000))

    new_list = [x + 1 for x in new_price_change_data]

    new_price_data = [100]

    # append new prices to list
    for i in range(1, len(new_list)):
        new_price_data.append(new_price_data[i - 1] * new_list[i])

    plt.plot(new_price_data)

    print(new_price_change_data)

    # plt.show()

    return new_price_change_data
