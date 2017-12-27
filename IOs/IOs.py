import pandas as pd
import time
from DataStruct.univariate_ts_with_anomaly import univariate_ts_with_anomaly

def read_time_series(file_path,index_col,dateparse,header_num):
    timeseries = pd.read_csv(file_path,header=header_num,index_col=index_col,date_parser=dateparse)
    return timeseries
    
    # TODO

def read_time_series_with_ananomly(
        file_path,name="noname",
        timeparse=None,
        header_num=0,
        index_col=0,
        value_col=1,
        ananomly_col=2,
        types_col=None
    ):
    timeparsefunction={
        "datetime":from_timestamp_to_datetime,
        "none":do_nothing
    }
    timeseries=pd.read_csv(file_path,header=header_num)
    timeseries=timeparsefunction.get(timeparse)(timeseries,index_col)
    return univariate_ts_with_anomaly(name=name,timeseries=timeseries.set_index(index_col),index=index_col,
                                      value=value_col,anomaly=ananomly_col,types=types_col)


def from_timestamp_to_datetime(timeseries,index_col):
    timeseries[index_col]=timeseries[index_col].map(lambda x: time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(x)))
    return timeseries

def do_nothing(timeseries,index_col):
    return timeseries

if __name__ == '__main__':
    filepath = "../dataset/anomaly_detection_1/train.csv"
    data = read_time_series_with_ananomly(file_path=filepath, timeparse="none", index_col="timestamp",
                                          header_num=0, ananomly_col="label",types_col="KPI ID",value_col="value")
    types = data.get_types()
    print(data.getPeriod(type="e0770391decc44ce",fft_size=1000))
    #print(data.get_types_number())
    #data.plot(type="e0770391decc44ce")
    #print(data.get_dataframe(type="e0770391decc44ce"))
    #for type in types:
     #   print(type+" "+str(data.anomaly_num(type=type))+" "+str(data.length(type=type)))
    #print("123")
