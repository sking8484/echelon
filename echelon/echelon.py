import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm

import datetime
import seaborn as sns

sns.set_style("darkgrid")







class EchelonBT():
    def __init__(self, stock_list, master_dataframe, weights,place_trades, long_only):

        self.stock_list = stock_list
        self.master_dataframe = master_dataframe
        self.weights = weights
        self.place_trades = place_trades
        self.long_only = long_only


    #create dataframes
    """HELPER FUNCTION NORMALIZING WEIGHTS CALLED FROM RUN"""
    def normalize_weights(self, row):
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
        print("WRITE YOUR OWN FUNCTION")
        pass




    def create_trade(self):
        if self.place_trades:
            #WRITE CODE TO GENERATE TRADES HERE
            print("TRADES WILL BE GENERATED HERE")



    def statistics(self):
        if self.statistics:
            #THIS IS WHERE THE STATISTICS AND PLOTS WILL BE GENERATED
            print("STATISTICS AND PLOTS WILL BE GENERATED HERE")
    def run(self):
        """NORMALIZING WEIGHTS"""
        self.weights = self.weights.apply(self.normalize_weights, axis = 1).fillna(0)
        print("Your weights have been normalized for a long only strategy")


        self.create_signals()
        self.create_trade()
        self.statistics()
