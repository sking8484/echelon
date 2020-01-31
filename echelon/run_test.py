import pandas as pd
from echelon import EchelonBT
from test_echelon import TestApp

data_master = pd.read_pickle('master_pricing_df')

stock_list = ['AAPL', 'GOOGL']
app_goog = data_master[stock_list]

weights_master = pd.DataFrame(index = app_goog.index)

num_periods = 10
for stock in stock_list:
    weights_master[stock] = (data_master[stock] - data_master[stock].shift(num_periods))/num_periods

print(weights_master)





app = TestApp(stock_list, "TEST", weights_master, False, True)
app.run()
