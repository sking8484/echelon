import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm

import datetime
import seaborn as sns

sns.set_style("darkgrid")







class EchelonBT():
    def __init__(self, stock_list = "Your Universe", master_dataframe = "Your Master DataFrame, Closes, OHLC, etc...", weights= "Weights DataFrame",place_trades= "BOOL", long_only= "BOOL"):

        """Initilialize the backtest.

        Example:

            **From echelon import EchelonBT

            class TestApp(EchelonBT):
                def __init__(self):
                    super().__init__()

                def create_signals():
                        Overwrite the create_signals class. This is where you write you own trading logic
                    .
                    .
                    .
        You will need to set 5 values after  instantiating your class, ex app = TestApp(EchelonBT)

        *****/*****
        The 5 arguments needed are:
            *stock_list::List
                Your universe, as a list

            *master_dataframe::DataFrame
                The DataFrame with your required data

            *weights::DataFrame
                The DataFrame with your weights.

            *place_trades::BOOL
                The order switch. True will send orders to your email, for now.

            *long_only::BOOL
                Helps when normalizing weights. If True, will convert negative weights to 0 before normalizing.
        *****/*****
        Set these values using the following syntax:
            app = TestApp()
            app.stock_list=stock_list
            .
            .
            .
            app.run()
        """

        self.stock_list = stock_list
        self.master_dataframe = master_dataframe
        self.weights = weights
        self.place_trades = place_trades
        self.long_only = long_only


    #create dataframes

    def normalize_weights(self, row):
        """HELPER FUNCTION NORMALIZING WEIGHTS CALLED FROM RUN"""
        if self.long_only:
            long_weights = []
            for x in row:
                if x<0:
                    long_weights.append(0)
                else:
                    long_weights.append(x)
            if sum(long_weights) == 0:
                return long_weights
            else:
                normalized = []
                for long_weight in long_weights:
                    normalized.append(long_weight/sum(long_weights))
                return normalized

    def create_signals(self):
        #USE THIS FUNCTION NAME TO CREATE YOUR SIGNALS
        """Overwrite this function. This function must return a dataframe of your returns, where columns are equal to your stock list and the values are the returns of your strategy.  Do NOT weight your returns. This will be done automatically using the weights you passed the class. Find an example below.

        *****/*****

        interim_df = pd.DataFrame(index = self.master_dataframe.index)
        trades_df = pd.DataFrame(index = self.master_dataframe.index)

        for x in self.stock_list:
            interim_df[x+'_pct_change'] = self.master_dataframe[x].pct_change()
            interim_df[x + 'MA'] = self.master_dataframe[x].rolling(window = 15).mean()

            signals = (interim_df[x+'MA']<self.master_dataframe[x])
            interim_df[x + 'trades'] = 0

            interim_df[x + 'trades'][signals] = interim_df[x+'_pct_change'].shift(-1)

            trades_df[x] = interim_df[x+'trades']

        return trades_df,signals

        """
        pass

    def create_trades(self):
        if self.place_trades:
            #WRITE CODE TO GENERATE TRADES HERE
            print("TRADES WILL BE GENERATED HERE")

    def statistics(self):
        if self.statistics:
            """

            This automatically creates statistics

            Currently including the position size as a percentage of your portfolio, your portfolio returns plotted as a chart, and your portfolio returns split into month and year plotted as a heatmap.

            In the works:
                Correlation Heatmap
                Rolling standard deviation of your Portfolio
                rolling sharpe of your portfolio
                rolling correlation to the sp500 your portfolio
                and more

            """
            #THIS IS WHERE THE STATISTICS AND PLOTS WILL BE GENERATED
            """FIND THE WEIGHTED RETURNS"""

            self.weighted_returns = pd.DataFrame(index = self.master_dataframe.index)

            for x in self.stock_list:
                self.weighted_returns[x] = self.returns[x]*self.weights[x]

            self.weighted_returns['Portfolio'] = np.sum(self.weighted_returns,axis = 1)

            """

            FIND THE RETURNS SPLIT BY YEAR AND MONTH

            """

            portfolio = self.weighted_returns[['Portfolio']]

            years = []
            months = []

            for date in portfolio.index:
                years.append(date.year)
                months.append(date.month)
            years = pd.Series(list(set(years))).sort_values()
            months = pd.Series(list(set(months))).sort_values(ascending=False)

            split_returns = np.zeros((len(months), len(years)))

            for j,year in enumerate(years):
                for i,month in enumerate(months):
                    month_interval = portfolio.loc[ str(month) + '-' + '01-'+ str(year):str(month) + '-28-' + str(year)]
                    try:
                        returns = month_interval.iloc[-1]/month_interval.iloc[0]

                    except:
                        returns = portfolio['Portfolio'].mean()
                    split_returns[i,j] = returns
            sns.heatmap(split_returns, yticklabels = months, xticklabels = years)





            """

            Plot some more statistics

            """

            plt.figure()
            plt.plot(self.weights)
            plt.plot(self.weighted_returns.cumsum())

            legend = []
            for x in self.weights.columns:
                legend.append(x)
            for y in self.weighted_returns.columns:
                legend.append(y)
            plt.legend(legend)

            plt.show()


    # def help(self):
    #     help_string = "****/****\nYou've asked for help. Smart.\n****/****\nInitializing:\n\tEchelonBT requires 5 arguments to be set.\n\t\tstock_list::List, your universe of stocks. \n\t\t\tUsed to iterate through your dataframes and create the necessary data.\
    #     "
    #     print(help_string)


    def run(self):
        """NORMALIZING WEIGHTS"""

        self.weights = self.weights.apply(self.normalize_weights, axis = 1).fillna(0)


        print("Your weights have been normalized for a long only strategy")

        """RUNNING FUNCTIONS"""
        self.returns = self.create_signals()
        self.create_trades()
        self.statistics()
