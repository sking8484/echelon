from echelon import EchelonBT


class TestApp(EchelonBT):
    def __init__(self):
        super().__init__()


    def create_signals(self):
        print("This came from TestApp's create signals")
        print(self.weights)
