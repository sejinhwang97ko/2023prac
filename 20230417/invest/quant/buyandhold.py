import numpy as np
from datetime import datetime
import pandas as pd
def bh(df,feature= 'Close',start = '20000101',end = '20230101'):
    # 인덱스 시계열로 변경
    df.index = pd.to_datetime(df.index)
    start = datetime.strptime(start, "%Y%m%d")
    end = datetime.strptime(end, "%Y%m%d")
    df = df.loc[start:end]
    df = df.loc[~df.isin([np.nan, np.inf, -np.inf]).any(1)]
    df_1 = df[[feature]]
    df_1['daily_rtn'] = df_1[feature].pct_change()
    df_1['st_rtn'] = (1 + df_1['daily_rtn']).cumprod()
    return df_1