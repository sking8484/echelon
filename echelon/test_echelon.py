from echelon import EchelonBT
import pandas as pd
import matplotlib.pyplot as plt


class TestApp(EchelonBT):
    def __init__(self):
        super().__init__()


    def create_signals(self):
        print("This came from TestApp's create signals")

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

        return trades_df
