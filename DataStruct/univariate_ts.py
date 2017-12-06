from DataStruct.ts import ts


class univariate_ts(ts):
    #attribute
    attribute=-1;
    length=0;

    def __init__(self,name,timeseries):
        self.name=name
        self.timeseries=timeseries

    def plot(self):
        return "todo"

    def ts_window(self,start,end):
        return "todo"