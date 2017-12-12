from utils import append_data,getStrs,SeriesStandard
import pandas as pd


def make_samples(idnames,time_series,value_series,anomaly_series,period):
    series = SeriesStandard(value_series)
    if period>len(series):
        return "error"
    result={}
    for start in range(period,len(series)):
        result = append_data(result,"id",idnames)
        result = append_data(result,"time",time_series[start])
        result = append_data(result,"label",anomaly_series[start])
        strs = getStrs("before",period+1)
        for i in range(period+1):
            result = append_data(result,strs[i],series[start-i])
    return pd.DataFrame(result)

def make_samples_without_label(idnames,time_series,value_series,period):
    series = SeriesStandard(value_series)
    if period > len(series):
        return "error"
    result = {}
    for start in range(period, len(series)):
        result = append_data(result, "id", idnames)
        result = append_data(result, "time", time_series[start])
        strs = getStrs("before", period + 1)
        for i in range(period + 1):
            result = append_data(result, strs[i], series[start - i])
    return pd.DataFrame(result)