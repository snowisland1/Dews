import pandas as pd
import matplotlib.pyplot as plt
from utils.utils import getPeriod

class univariate_ts_with_anomaly():

    def __init__(self, name, timeseries,index,value,anomaly,types):
        #todo parameter checkout
        self.name = name
        self.timeseries = timeseries
        self.index = index
        self.value = value
        self.anomaly = anomaly
        self.types = types
        self.period = -1

    def get_dataframe(self,type):
        return self.timeseries

    def get_types(self):
        if(self.types == None):
            return None
        else:
            return pd.unique(self.timeseries[self.types])

    def get_types_number(self):
        return len(pd.unique(self.timeseries[self.types]))

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

    def anomaly_num(self,type=None):
        if(type==None):
            return len(self.timeseries[self.timeseries[self.anomaly] == 1])
        else:
            timeseries = self.timeseries[self.timeseries[self.types] == type]
            return len(timeseries[timeseries[self.anomaly] == 1])

    def length(self,type=None):
        if (type == None):
            return len(self.timeseries)
        else:
            timeseries = self.timeseries[self.timeseries[self.types] == type]
            return len(timeseries)

    def getPeriod(self,type=None,fft_size=None):
        ts = None
        if (type == None):
            ts=self.timeseries.loc[:,[self.index,self.value]]
        else:
            ts = self.timeseries[self.timeseries[self.types] == type].loc[:,[self.index,self.value]]
        return getPeriod(ts,self.index,self.value,fft_size)

    def __getattr__(self, item):
        return "default"