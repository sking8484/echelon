import pandas as pd
from echelon import EchelonBT
from test_echelon import TestApp
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

data_master = pd.read_pickle('master_pricing_df')

stock_list = ['AAPL', 'GOOGL', 'GE', 'LUV']
app_goog = data_master[stock_list]

weights_master = pd.DataFrame(index=app_goog.index)

#num_periods = 10
#for stock in stock_list:


num_periods = np.linspace(2,33,30)
rolling_windows = np.linspace(2,33,30)


returns_df = np.zeros((len(num_periods),len(rolling_windows)))

def backtest():
    app = TestApp()
    for i,num_period in enumerate(num_periods):

        for stock in stock_list:
            weights_master[stock] = (data_master[stock].shift(1) - data_master[stock].shift(int(num_period))) /data_master[stock].shift(int(num_period))
        for j,rolling_window in enumerate(rolling_windows):





            app.stock_list = stock_list
            app.master_dataframe = app_goog
            app.weights = weights_master
            app.place_trades = False
            app.long_only = True
            app.optimize = True
            app.stats = False
            app.num_periods = num_period
            app.rolling_window = rolling_window




            app.run()
            returns_df[i,j] = app.portfolio.iloc[-1]
        print(returns_df)



backtest()
