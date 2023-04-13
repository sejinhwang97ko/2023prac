import pandas as pd
import numpy as np
from datetime import datetime


class Invest():
    # 생성자 함수 생성

    def  __init__(self, _df, _col):
        # self 변수는 클래스 각각의 독립적인 변수
        self.df = _df
        self.col = _col

    def func_1(self, start, end):
        # 인덱스를 시계열로 변경
        self.df.index= pd.to_datetime(self.df.index)
        # start, end를 시계열로 변경
        start = datetime.strptime(start, "%Y%m%d").isoformat()
        end = datetime.strptime(end, "%Y%m%d").isoformat()
        
        self.df = self.df.loc[~self.df.isin([np.nan, np.inf, -np.inf]).any(1), [self.col]]
        self.df['center'] = self.df[self.col].rolling(20).mean()
        # ub, lb 두개의 파생변수 생성
        # 이동 평균선 + (2 * 데이터 20개의 표준편차)
        std = self.df[self.col].rolling(20).std()
        self.df['ub']  = self.df['center'] + (2 * std)
        self.df['lb']  = self.df['center'] - (2 * std)
        # 데이터를 시간 시간부터 종료 시간까지 필터
        self.df = self.df.loc[start:end]

        return self.df

    def func_2(self):
        # 거래 내역이라는 파생변수
        self.df['trade'] = ""

        for i in self.df.index:
            if self.df.loc[i, self.col] > self.df.loc[i, 'ub']:
                if self.df.shift(1).loc[i, 'trade'] == 'buy':
                    self.df.loc[i, 'trade'] = ''
                else:
                    self.df.loc[i, 'trade'] = ''
            elif self.df.loc[i, self.col] < self.df.loc[i, 'lb']:
                if self.df.shift(1).loc[i, 'trade'] == 'buy':
                    self.df.loc[i, 'trade'] = 'buy'
                else:
                    self.df.loc[i, 'trade'] = 'buy'
            else:
                if self.df.shift(1).loc[i, 'trade'] == 'buy':
                    self.df.loc[i, 'trade'] = 'buy'
                else:
                    self.df.loc[i, 'trade'] = ''

        return self.df

    # 3. 세 번째 함수를 생성(매개변수 데이터프레임 하나)
    #     1. 수익율 파생변수 생성 값은 "1"
    #     2. 판매를 한 날의 수익율 변경
    #     3. 누적 수익율을 계산하여 새로운 파생변수를 생성
    #     4. 최종 누적 수익율을 출력(print)
    def func_3(self):
        self.df['return'] = 1
        rtn = 1.0
        buy = 0.0
        sell = 0.0

        for i in self.df.index:
            if (self.df.shift(1).loc[i, 'trade'] == '') and (self.df.loc[i, 'trade'] == 'buy'):
                buy = self.df.loc[i, self.col]
                print('진입일:' , i, '구매 가격:' , buy)
            elif (self.df.shift(1).loc[i, 'trade'] == 'buy') and (self.df.loc[i, 'trade'] == ''):
                sell = self.df.loc[i, self.col]
                rtn = (sell -buy) / buy + 1
                self.df.loc[i, 'return'] = rtn
                print('판매일:' , i, '판매 가격:' , sell, '수익율:', rtn)

            if self.df.loc[i, 'trade'] == '':
                buy = 0.0
                sell = 0.0

        # 누적 수익율
        acc_rtn = 1.0

        for i in self.df.index:
            rtn = self.df.loc[i, 'return']
            acc_rtn *= rtn
            self.df.loc[i, 'acc_rtn'] = acc_rtn

        print('누적 수익율: ', acc_rtn)
        
        return self.df