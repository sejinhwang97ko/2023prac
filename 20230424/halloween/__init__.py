# class 선언 Halloween
# 생성자 함수에서 데이터프레임, 시작년도, 종료년도 매개변수
# self변수를 생성, self.acc_rtn 변수는 1 고정

# 누적 수익율 계산하는 함수 (accrtn)

# CAGR을 계산하는 함수(cagr) (투자기간은 종료년도 - 시작년도)
import pandas as pd

class Halloween:
    # 생성자 함수
    def __init__(self, df, start, end):
        self.df = df
        self.start = start
        self.end = end
        self.acc_rtn = 1

    def accrtn(self):
        if 'Date' in self.df.columns:
            self.df['Date'] = pd.to_datetime(self.df['Date'], format="%Y-%m-%d")
            self.df.set_index('Date', inplace=True)

        for i in range(self.start, self.end):
            self.buy_mon = str(i) + "-11" # 공동 아니게 하기 위해서 self.를 붙임
            self.sell_mon = str(i+1) + "-04"

            self.buy = self.df.loc[self.buy_mon].iloc[0]['Open']
            self.sell = self.df.loc[self.sell_mon].iloc[-1]['Close']

            # 수익율
            self.rtn = (self.sell - self.buy) / self.buy + 1
            self.acc_rtn *= self.rtn
        return self.acc_rtn

    def cagr(self):
        self.due = self.end - self.start
        self.CAGR = (self.acc_rtn ** (1/self.due)) -1
        return (self.CAGR * 100)
