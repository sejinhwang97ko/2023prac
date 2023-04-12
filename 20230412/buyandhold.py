import numpy as np
from datetime import datetime

def bh(df,feature,start,end):
    start = datetime.strptime(start, "%Y%m%d").isoformat()
    end = datetime.strptime(end, "%Y%m%d").isoformat()
    df = df.loc[start:end]
    df = df.loc[~df.isin([np.nan, np.inf, -np.inf]).any(1)]
    df_1 = df[[feature]]
    df_1['daily_rtn'] = df_1[feature].pct_change()
    df_1['st_rtn'] = (1 + df_1['daily_rtn']).cumprod()
    return df_1