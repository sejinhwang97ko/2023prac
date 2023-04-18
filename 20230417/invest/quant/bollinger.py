import pandas as pd
import numpy as np
from datetime import datetime

def func_1(df, col='Close', start = '20100101', end = '20230101'):
    # 인덱스를 시계열로 변경
    df.index= pd.to_datetime(df.index)
    # start, end를 시계열로 변경
    start = datetime.strptime(start, "%Y%m%d").isoformat()
    end = datetime.strptime(end, "%Y%m%d").isoformat()
    
    df = df.loc[~df.isin([np.nan, np.inf, -np.inf]).any(1), [col]]
    df['center'] = df[col].rolling(20).mean()
    # ub, lb 두개의 파생변수 생성
    # 이동 평균선 + (2 * 데이터 20개의 표준편차)
    std = df[col].rolling(20).std()
    df['ub']  = df['center'] + (2 * std)
    df['lb']  = df['center'] - (2 * std)
    # 데이터를 시간 시간부터 종료 시간까지 필터
    df = df.loc[start:end]

    return df