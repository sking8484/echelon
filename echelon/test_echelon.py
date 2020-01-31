from echelon import EchelonBT


class TestApp(EchelonBT):
    def __init__(self,stock_list,master_dataframe,weights, place_trades,long_only):
        super().__init__(stock_list,master_dataframe,weights, place_trades, long_only)

    def create_signals(self):
        print("This came from TestApp's create signals")
