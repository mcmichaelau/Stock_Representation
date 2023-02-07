import numpy as np
from scipy.optimize import minimize
from price_generator import get_prices

input_price_change_data = get_prices('AAPL', 10000)


def objective_function(weights_array, price_change_data):
    # create price values from price change data
    price_multiplication_list = [x + 1 for x in price_change_data]

    # income
    initial_funds = 1000
    monthly_income = 500
    invested_assets = 500
    cash_assets = [initial_funds - invested_assets]
    portfolio_value = [initial_funds]

    # initialize lists
    total_percentage_list = [price_multiplication_list[0]]

    invested_assets = [invested_assets * price_multiplication_list[0]]

    percent_invested = [invested_assets[0] / portfolio_value[0]]

    # track days
    day_counter = 0

    # track total cash invested
    total_cash_invested = initial_funds

    # track buy and hold value
    buy_and_hold = [initial_funds]

    start_value = int(len(weights_array)/2)

    # loop through price change data
    for i in range(1, len(price_change_data)):

        # update stock gain total percentage list
        total_percentage_list.append(total_percentage_list[i - 1] * price_multiplication_list[i])

        if i < start_value:

            # print('----------------------')

            # update invested assets
            invested_assets.append(invested_assets[i-1])

            # update buy and hold value
            buy_and_hold.append(buy_and_hold[i - 1])

            # update cash assets
            cash_assets.append(cash_assets[i - 1])

            # update percent invested
            percent_invested.append(0)

            # update portfolio value
            portfolio_value.append(portfolio_value[i - 1])

            # print(i)

        elif i >= start_value:
            # update invested assets
            invested_assets.append(invested_assets[i - 1] * price_multiplication_list[i])

            # update buy and hold value
            buy_and_hold.append(buy_and_hold[i - 1] * price_multiplication_list[i])
            # print(f'buy and hold: {buy_and_hold[i]}')

            # print(f'invested assets: {invested_assets[i]}')

            # add a day counter
            day_counter += 1

            # if day counter is 21, reset day counter and add monthly income
            if day_counter == 21:

                # reset day counter
                day_counter = 0

                # add income to cash assets
                cash_assets.append(cash_assets[i - 1] + monthly_income)

                # add income to buy and hold value
                buy_and_hold[i] += monthly_income
                # print(f'added to buy and hold: {buy_and_hold[i]}')

                total_cash_invested += monthly_income

            else:
                # keep cash the same
                cash_assets.append(cash_assets[i - 1])

            # update portfolio value
            portfolio_value.append(invested_assets[i] + cash_assets[i])
            # print(f'movement: {price_multiplication_list[i]}')
            # print(f'cash assets: {cash_assets[i]}')
            # print(f'portfolio value: {portfolio_value[i]}')

            # percentage of portfolio invested
            percent_invested.append(invested_assets[i] / portfolio_value[i])
            # print(f'percent invested: {percent_invested[i]}')

            # start data collection for sigmoid at the beginning of data

            # calculate sigmoid value
            sigmoid_value = 0
            for j in range(0, start_value, 2):
                # print(weights_array[j + 1])
                sigmoid_value += (weights_array[j] * price_change_data[i - j] + weights_array[j+1])

            # print(f'sigmoid value: {sigmoid_value}')

            # get allocation decision from sigmoid function. must be greater than or equal to current investment
            # percentage (no selling)
            percent_invested[i] = (1 / (1 + np.exp(-(percent_invested[i] + sigmoid_value))))
            # print(f'new percent invested: {percent_invested[i]}')

            # update invested assets (buy)
            invested_assets[i] = portfolio_value[i] * percent_invested[i]

            # update cash assets
            cash_assets[i] = portfolio_value[i] - invested_assets[i]

            # update portfolio value
            portfolio_value[i] = invested_assets[i] + cash_assets[i]
            # print(f'invested assets: {invested_assets[i]}')
            # print(f'cash assets: {cash_assets[i]}')
            # print(f'portfolio value: {portfolio_value[i]}')

    print(f'buy and hold value: {buy_and_hold[-1]}')
    # print(portfolio_value)
    # total cash invested
    print(f'total cash invested: {total_cash_invested}')

    # stock percent gain
    stock_percent_gain = (total_percentage_list[-1] - 1) * 100
    print(f'stock percent gain: {round(stock_percent_gain, 2)}%')

    # buy and hold percent gain
    buy_and_hold_percent_gain = ((buy_and_hold[-1] - total_cash_invested) / total_cash_invested) * 100
    print(f'buy and hold percent gain: {round(buy_and_hold_percent_gain, 2)}%')

    # portfolio percent gain
    portfolio_percent_gain = ((portfolio_value[-1] - total_cash_invested) / total_cash_invested) * 100
    print(f'portfolio percent gain: {round(portfolio_percent_gain, 2)}%')

    # print(f"total_percentage_list: {total_percentage_list}")
    # print(f"total_percentage_list2: {total_percentage_list2}")
    # print('------')
    # print('------')
    # print('------')
    # print('------')
    # print(f"buy immediately percent gain: {round(buy_immediately_percent_gain, 2)} %")
    # print(f"stock percent gain: {round(stock_percent_gain, 2)} %")
    # print(f"portfolio percent gain: {round(portfolio_percent_gain, 2)} %")
    # print(f"total cash invested: {total_cash_invested}")

    return -portfolio_percent_gain


# test = objective_function([1, 1, 1, 1], input_price_change_data)
price_data = tuple(input_price_change_data)

initial_weights = np.ones(10)

res = minimize(objective_function, x0=initial_weights, method='SLSQP', args=(price_data,))
print('----------- Weights -----------')
print(list(res.x))
