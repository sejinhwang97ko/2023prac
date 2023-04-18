import pandas as pd
import numpy as np
from datetime import datetime

def func_1(df, col='Close',start = '20100101',end= '20230101'):
    #인덱스가 Date가 아니면? Date 컬럼을 인덱스로 변경
    if 'Date' in df.columns:
        df = df.set_index("Date")
    #start, end를 시계열로 변경
    start = datetime.strptime(start, "%Y%m%d").isoformat()
    end = datetime.strptime(end , "%Y%m%d").isoformat()

    df = df.loc[~df.isin([np.nan, np.inf, -np.inf]).any(1)]
    df = df[[col]]
    df.index= pd.to_datetime(df.index)

    # 새로운 파생변수 년-월의 데이터를 대입
    def change(x):
        return datetime.strftime(x, '%Y-%m')

    df['STD-YM'] = list(map(change, df.index))

    df = df.loc[start:end]

    # 혹은 df['STD-YM'] = list(map(lambda x: datetime.strftime(x, '%Y-%m'), df.index))
    return df

def func_2(df):
    col = df.columns[0]
    # df2 = pd.DataFrame()
    # _list = df['STD-YM'].unique()

    # for i in _list:
    #     last_df = df.loc[df['STD-YM'] == i].tail(1)
    #     df2 = pd.concat([df2, last_df])

    df2 = df.loc[df['STD-YM'] != df['STD-YM'].shift(-1)]
    
    df2['BF_1M'] = df2[col].shift(1)
    df2['BF_1M'].fillna(0, inplace=True)
    df2['BF_12M'] = df2[col].shift(12)
    df2['BF_12M'].fillna(0, inplace=True)
    return df2

def func_3(df1,df2):
    df1['trade'] =''
    df1['return'] =1
    col = df1.columns[0]

    # 거래 내역 추가
    # 구매 조건 -> ((전월 종가/ 전년도 종가) -1)의 값이 0보다 크고 무한대가 아닌 경우
    # 분자가 크면 사겠다.
    for i in df2.index:
        signal = ""

        # 절대 모멘텀 계산
        momentum_index = df2.loc[i,'BF_1M']/df2.loc[i,'BF_12M'] -1

        # 절대 모멘텀 지표에 따라서 True/False로 구분
        flag = True if((momentum_index > 0) & (momentum_index != -np.inf) & (momentum_index != np.inf)) else False

        if flag:
            signal = 'buy'
        
        #print('날짜 : ', i, "모멘텀 인덱스: ", momentum_index, "flag: ", flag, "signal: ", signal)

        df1.loc[i,'trade'] = signal

    rtn = 1.0
    buy = 0
    sell = 0

    for i in df1.index:
        # 구매한 날을 체크, 구매가 지정
        if (df1.loc[i,'trade'] == 'buy') and (df1.shift(1).loc[i,'trade'] ==""):
            buy = df1.loc[i, col]
            print("진입일: ", i, "진입가격: ", buy)
        elif (df1.shift(1).loc[i,'trade'] == 'buy') and (df1.loc[i,'trade'] ==""):
            sell = df1.loc[i, col]
            rtn = (sell -buy) / buy + 1
            df1.loc[i, 'return'] = rtn
            print("판매일: ", i, "판매가격: ", sell, '수익율: ', rtn)

    acc_rtn = 1.0
    df1['acc_rtn'] = 1

    for i in df1.index:
        acc_rtn *= df1.loc[i,'return']
        df1.loc[i,'acc_rtn'] = acc_rtn
    print(acc_rtn)

    return df1