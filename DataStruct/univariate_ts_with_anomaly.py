import pandas as pd
import matplotlib.pyplot as plt
from utils.utils import getPeriod

class univariate_ts_with_anomaly():
    # attribute
    period = -1#周期

    def __init__(self, name, timeseries,index,value,anomaly,types):
        #todo 参数检查
        self.name = name
        self.timeseries = timeseries
        self.index = index
        self.value = value
        self.anomaly = anomaly
        self.types = types

    def get_dataframe(self,type):
        return self.timeseries

    def get_types(self):
        if(self.types == None):
            return None
        else:
            return pd.unique(self.timeseries[self.types])

    def get_types_number(self):
        return len(pd.unique(self.timeseries[self.types]))

    #实现打印出时间序列和异常点
    def plot(self,type):
        timeseries = self.timeseries[self.timeseries[self.types]==type]
        self.plot_timeseries(timeseries)

    def plot_timeseries(self,timeseries):
        plt.plot(timeseries.loc[:,self.value],color="blue")
        timeseries_ano=timeseries[timeseries[self.anomaly]==1]
        plt.plot(timeseries_ano.index,timeseries_ano.loc[:,self.value],"r.")
        plt.title("timeseries plot")
        plt.show(block=False)

    def ts_window(self, start, end,type):
        return "todo"

    #返回异常点的数目
    def anomaly_num(self,type=None):
        if(type==None):
            return len(self.timeseries[self.timeseries[self.anomaly] == 1])
        else:
            timeseries = self.timeseries[self.timeseries[self.types] == type]
            return len(timeseries[timeseries[self.anomaly] == 1])

    #返回整个时间序列的长度
    def length(self,type=None):
        if (type == None):
            return len(self.timeseries)
        else:
            timeseries = self.timeseries[self.timeseries[self.types] == type]
            return len(timeseries)

    #返回时间序列的周期
    def getPeriod(self,type=None,fft_size=None):
        ts = None
        if (type == None):
            ts=self.timeseries.loc[:,[self.index,self.value]]
        else:
            ts = self.timeseries[self.timeseries[self.types] == type].loc[:,[self.index,self.value]]
        return getPeriod(ts,self.index,self.value,fft_size)

    def __getattr__(self, item):
        return "default"