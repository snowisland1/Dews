from utils import append_data,getStrs
import pandas as pd

def make_samples(series,anomaly_series,period):
    if period>len(series):
        return "error"
    result={}
    for start in range(period,len(series)):
        result = append_data(result,"label",anomaly_series[start])
        strs = getStrs("before",period+1)
        for i in range(period+1):
            result = append_data(result,strs[i],series[start-i])
    return pd.DataFrame(result)