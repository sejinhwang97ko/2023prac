from invest.quant import momentum as mn
from invest.quant import buyandhold as bnh
# from invest.quant import bollinger as boll

class Invest:

    # 생성자 함수
    def __init__(self, _df, _col='Close', _start = '20100101', _end = '20230101'):
        self.df = _df
        self.col = _col
        self.start = _start
        self.end = _end

    def momentum(self):
        self.df1 = mn.func_1(self.df, self.col, self.start, self.end)
        self.df2 = mn.func_2(self.df1)
        self.result = mn.func_3(self.df1, self.df2)
        return self.result

    def buyandhold(self):
        self.result = bnh.bh(self.df, self.col, self.start, self.end)
        return self.result

    # def bollinger(self):
    #     self.result = boll.create_band(self.df, self.col, self.start, self.end)
    #     self.result = boll.add_trade(self.result)
    #     self.result = boll.add_rtn(self.result)
    #     return self.result