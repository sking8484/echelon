import plotly.graph_objs as go
import dash_html_components as html
import dash_core_components as dcc
import dash
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm

import datetime
import seaborn as sns
sns.set_style("darkgrid")


class EchelonBT():
    def __init__(self, stock_list="Your Universe", master_dataframe="Your Master DataFrame, Closes, OHLC, etc...", weights="Weights DataFrame", place_trades=False, long_only=True):
        """Initilialize the backtest.

        ******** Any DataFrame that you pass MUST have columns equal to self.stock_list

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
        self.optimize = False

    # create dataframes

    def signal_weights(self):
        """*****/*****

        Multiplies your weights by the signals given. Signals is returned from the create signals function. The columns must be equal to the stock list.

        *****/*****"""
        self.weights.fillna(0, inplace=True)
        weighted_signals = pd.DataFrame(index=self.master_dataframe.index)
        for stock in self.stock_list:
            weighted_signals[stock] = self.weights[stock] * self.signals[stock]

        return weighted_signals

    def normalize_weights(self, row):
        """*****/*****

        HELPER FUNCTION NORMALIZING WEIGHTS CALLED FROM RUN

        *****/*****"""
        if self.long_only:

            long_weights = []
            for x in row:
                if x < 0:
                    long_weights.append(0)
                else:
                    long_weights.append(x)
            if sum(long_weights) == 0:
                return long_weights
            else:
                normalized = []
                for long_weight in long_weights:
                    normalized.append(long_weight / sum(long_weights))
                return normalized

    def create_signals(self):
        # USE THIS FUNCTION NAME TO CREATE YOUR SIGNALS
        """
        *****/*****

        Overwrite this function. This function must return two dataframes.
            1.) The returns of the trades in a dataframe.
                a.) These should not be cumualtive
                b.) The columns need to equal the stock list columns
            2.) The signals
                a.) The columns need to equal the stock list columns
                b.) this will be used to calculate the portfolio weights
         Find an example below.

        *****/*****
        *****/*****

        interim_df = pd.DataFrame(index = self.master_dataframe.index)
        trades_df = pd.DataFrame(index = self.master_dataframe.index)
        signals_df = pd.DataFrame(index = self.master_dataframe.index)

        for x in self.stock_list:
            interim_df[x+'_pct_change'] = self.master_dataframe[x].pct_change().shift(-1)
            interim_df[x + 'MA'] = self.master_dataframe[x].rolling(window = 15).mean()

            signals = (interim_df[x+'MA']<self.master_dataframe[x])
            signals_df[x] = signals
            interim_df[x + 'trades'] = 0

            interim_df[x + 'trades'][signals] = (interim_df[x+'_pct_change'][signals])




            trades_df[x] = interim_df[x+'trades']

        return trades_df,signals_df
        *****/*****

        """
        pass

    def create_trades(self):
        if self.place_trades:
            # WRITE CODE TO GENERATE TRADES HERE
            print("TRADES WILL BE GENERATED HERE")

    def statistics(self):
        """

        *****/*****

        This automatically creates statistics

        Currently including the position size as a percentage of your portfolio, your portfolio returns plotted as a chart, and your portfolio returns split into month and year plotted as a heatmap.

        In the works:
            Correlation Heatmap
            Rolling standard deviation of your Portfolio
            rolling sharpe of your portfolio
            rolling correlation to the sp500 your portfolio
            and more

        *****/*****
        *****/*****

        *****/*****
        *****/*****
        If you would like to optimize, follow the below code. In your overwritten function, add something in like this, where self.rolling_window was passed in.

        for x in self.stock_list:
            interim_df[x + '_pct_change'] = self.master_dataframe[x].pct_change().shift(-1)
            interim_df[x +
                       'MA'] = self.master_dataframe[x].rolling(window=int(self.rolling_window)).mean()


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

        """
        if self.optimize:
            self.weighted_returns = pd.DataFrame(
            index=self.master_dataframe.index)

            for x in self.stock_list:
                self.weighted_returns[x] = self.returns[x] * self.weights[x]

            self.weighted_returns['Portfolio'] = np.sum(
                self.weighted_returns, axis=1)

            portfolio = self.weighted_returns[['Portfolio']].cumsum()
            self.portfolio = portfolio

        if self.stats:
            # THIS IS WHERE THE STATISTICS AND PLOTS WILL BE GENERATED
            """FIND THE WEIGHTED RETURNS"""

            self.weighted_returns = pd.DataFrame(
                index=self.master_dataframe.index)

            for x in self.stock_list:
                self.weighted_returns[x] = self.returns[x] * self.weights[x]

            self.weighted_returns['Portfolio'] = np.sum(
                self.weighted_returns, axis=1)

            """

            FIND THE RETURNS SPLIT BY YEAR AND MONTH

            """

            portfolio = self.weighted_returns[['Portfolio']].cumsum()
            self.portfolio = portfolio


            self.years = []
            self.months = []

            for date in portfolio.index:

                self.years.append(date.year)
                self.months.append(date.month)

            self.years = pd.Series(list(set(self.years))).sort_values()
            self.months = pd.Series(
                list(set(self.months))).sort_values(ascending=False)

            split_returns = np.zeros((len(self.months), len(self.years)))

            for j, year in enumerate(self.years):
                for i, month in enumerate(self.months):
                    month_interval = portfolio.loc[str(
                        month) + '-' + '01-' + str(year):str(month) + '-28-' + str(year)]
                    try:
                        returns = (
                            month_interval.iloc[-1] / month_interval.iloc[0]) - 1

                        if returns.values[0] > (portfolio['Portfolio'].pct_change().dropna()[1:].mean() * 20) + (4 * portfolio['Portfolio'].pct_change().dropna()[1:].std()):

                            returns = 0

                    except Exception as e:
                        print(e)
                        returns = portfolio['Portfolio'].pct_change().dropna()[
                            1:].mean()
                    split_returns[i, j] = returns
            self.returns_month_year = split_returns

            """

            Plot the statistics

            """
            if not self.optimize:

                self.plot()

    def plot(self):

        app = dash.Dash()

        app.layout = html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id='portfolio_correlation',
                                  figure={'data':
                                          [
                                              go.Heatmap(
                                                  z=self.weighted_returns.corr().values, x=self.weighted_returns.corr().columns, y=self.weighted_returns.corr().columns, name='Correlation', colorscale='Jet'
                                              )
                                          ],
                                          'layout':go.Layout(title='Correlation of Assets in portfolio')
                                          }
                                  )
                    ], style={'width': '25%', 'display': 'inline-block'}),

                html.Div([dcc.Graph(id='portfolio_returns',
                                    figure={'data': [go.Scatter(y=self.weighted_returns['Portfolio'].cumsum(), x=self.weighted_returns.index, name='Portfolio'
                                                                )], 'layout':go.Layout(title='Portfolio Returns')
                                            }
                                    )], style={'width': '50%', 'display': 'inline-block'}),
                html.Div([
                    dcc.Graph(id='month_year_map',                                                                                              figure={'data': [
                        go.Heatmap(
                            z=self.returns_month_year, x=self.years, y=self.months,
                            colorscale='Jet')
                    ], 'layout':go.Layout(title='Returns by Time')})], style={'width': '25%', 'display': 'inline-block'}),

                dcc.Graph(id='stock_returns',
                          figure={'data': [go.Scatter(y=self.weighted_returns[stock].cumsum(), x=self.weighted_returns.index, name=stock
                                                      )for stock in self.weighted_returns.columns[:-1]], 'layout':go.Layout(title='stock_returns')
                                  }
                          ), dcc.Graph(id="weights",
                                       figure={'data': [go.Scatter(y=self.weights[stock], x=self.weights.index, name=stock)
                                                        for stock in self.stock_list], 'layout':go.Layout(title='Weights')}

                                       )
            ])

        app.run_server()

    def run(self):
        """NORMALIZING WEIGHTS"""

        print("Your weights have been normalized for a long only strategy")

        """RUNNING FUNCTIONS"""
        self.returns, self.signals = self.create_signals()

        self.weights = self.signal_weights()
        self.weights = self.weights.apply(
            self.normalize_weights, axis=1).fillna(0)

        self.create_trades()
        self.statistics()
