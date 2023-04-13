import pandas as pd
import numpy as np
from datetime import datetime

def func_1(df, col, start, end):
    # 인덱스를 시계열로 변경
    df.index= pd.to_datetime(df.index)
    # start, end를 시계열로 변경
    start = datetime.strptime(start, "%Y%m%d").isoformat()
    end = datetime.strptime(end, "%Y%m%d").isoformat()
    
    price_df = df.loc[~df.isin([np.nan, np.inf, -np.inf]).any(1), [col]]
    price_df['center'] = price_df[col].rolling(20).mean()
    # ub, lb 두개의 파생변수 생성
    # 이동 평균선 + (2 * 데이터 20개의 표준편차)
    std = price_df[col].rolling(20).std()
    price_df['ub']  = price_df['center'] + (2 * std)
    price_df['lb']  = price_df['center'] - (2 * std)
    # 데이터를 시간 시간부터 종료 시간까지 필터
    price_df = price_df.loc[start:end]

    return price_df

def func_2(price_df, col = 'Adj Close'):
    # 기준이 되는 컬럼이 무엇인가?
    # 기준이 되는 컬럼은 컬럼 중에서 첫번째 이기 때문에
    col = price_df.columns[0]
    # 거래 내역이라는 파생변수
    price_df['trade'] = ""

    for i in price_df.index:
        if price_df.loc[i, col] > price_df.loc[i, 'ub']:
            if price_df.shift(1).loc[i, 'trade'] == 'buy':
                price_df.loc[i, 'trade'] = ''
            else:
                price_df.loc[i, 'trade'] = ''
        elif price_df.loc[i, col] < price_df.loc[i, 'lb']:
            if price_df.shift(1).loc[i, 'trade'] == 'buy':
                price_df.loc[i, 'trade'] = 'buy'
            else:
                price_df.loc[i, 'trade'] = 'buy'
        else:
            if price_df.shift(1).loc[i, 'trade'] == 'buy':
                price_df.loc[i, 'trade'] = 'buy'
            else:
                price_df.loc[i, 'trade'] = ''

    return price_df

# 3. 세 번째 함수를 생성(매개변수 데이터프레임 하나)
#     1. 수익율 파생변수 생성 값은 "1"
#     2. 판매를 한 날의 수익율 변경
#     3. 누적 수익율을 계산하여 새로운 파생변수를 생성
#     4. 최종 누적 수익율을 출력(print)
def func_3(price_df2, col = 'Adj Close'):
    col = price_df2.columns[0]
    price_df2['return'] = 1
    rtn = 1.0
    buy = 0.0
    sell = 0.0

    for i in price_df2.index:
        if (price_df2.shift(1).loc[i, 'trade'] == '') and (price_df2.loc[i, 'trade'] == 'buy'):
            buy = price_df2.loc[i, col]
            print('진입일:' , i, '구매 가격:' , buy)
        elif (price_df2.shift(1).loc[i, 'trade'] == 'buy') and (price_df2.loc[i, 'trade'] == ''):
            sell = price_df2.loc[i, col]
            rtn = (sell -buy) / buy + 1
            price_df2.loc[i, 'return'] = rtn
            print('판매일:' , i, '판매 가격:' , sell, '수익율:', rtn)

        if price_df2.loc[i, 'trade'] == '':
            buy = 0.0
            sell = 0.0

    # 누적 수익율
    acc_rtn = 1.0

    for i in price_df2.index:
        rtn = price_df2.loc[i, 'return']
        acc_rtn *= rtn
        price_df2.loc[i, 'acc_rtn'] = acc_rtn

    print('누적 수익율: ', acc_rtn)
    
    return price_df2